import socket, threading
#use http://localhost:8000/test.html to test the server
HOST, PORT = 'localhost', 8000

BUFFER_SIZE = 1024

# create the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen(1)
print(f"Server is currently running on {HOST}:{PORT}")

# Function to generate HTTP response headers
def generate_response_header(code):

    header = {

        200: "HTTP/1.1 200 OK\n\n",

        304: "HTTP/1.1 304 Not Modified\n\n",

        400: "HTTP/1.1 400 Bad Request\n\n",

        403: "HTTP/1.1 403 Forbidden\n\n",

        404: "HTTP/1.1 404 Not Found\n\n",

        411: "HTTP/1.1 411 Length Required\n\n",
        
    }

    #default return
    return header.get(code, "HTTP/1.1 500 Internal Server Error\n\n")

# Handle client request
def client_requests(connection, address):
    try:
        request = connection.recv(BUFFER_SIZE).decode()

        lines = request.split('\n')

        request_line = lines[0]

        print(f"Request: {request_line} from {address}")
        
        method, path, _ = request_line.split()
        
        # match status codes to the errors
        response_code = {
            "/test.html": 200,

            "/": 304,

            "/bad": 400,

            "/forbidden": 403,

            "/notfound": 404,

            "/length": 411,

        }.get(path, 404)
        
        header = generate_response_header(response_code)

        response = header.encode()

        if response_code == 200:

            with open('test.html', 'rb') as file:

                response += file.read()
        
        connection.sendall(response)

    except Exception as e:

        print(f"Error: {e}")

    finally:

        connection.close()

# Main
try:

    while True:

        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=client_requests, args=(client_connection, client_address))
        client_thread.start()

except KeyboardInterrupt:

    print("Server is shutting down.")
    
    server_socket.close()

#references
#https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use
#https://realpython.com/python-sockets/
#https://stackoverflow.com/questions/28521261/python-socket-programming-simple-web-server
#https://stackoverflow.com/questions/10091271/how-can-i-implement-a-simple-web-server-using-python-without-using-any-libraries