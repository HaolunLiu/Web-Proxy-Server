import socket, logging, time, threading
from threading import Lock

cache = {}
cacheLock = Lock() 


def parseRequest(request):
    defaultPort = 80

    lines = request.split('\n')
    header = next((line for line in lines if line.startswith('Host:')), None)

    if header:

        _, host = header.split(': ')
        hostParts = host.strip().split(':')

        endHost = hostParts[0]
        endPort = int(hostParts[1]) if len(hostParts) > 1 else defaultPort

        return endHost, endPort

    return None, None

def fixRequest(request):
    lines = request.split('\n')
    requestLine = lines[0]
    parts = requestLine.split(' ')

    if len(parts) >= 3:
        method, url, http = parts
        path = url.split('://')[-1]  
        path = '/' + path.split('/', 1)[-1]  
        newRequest = f"{method} {path} {http}"
        lines[0] = newRequest

    return '\n'.join(lines)

def connection(clientCon):
    try:
        timeStart = time.time()
        request = clientCon.recv(1024).decode()
        request = fixRequest(request)

        endHost, endPort = parseRequest(request)
        url = request.split(' ')[1]

        data = b''

        if url in cache:
            logging.info(f"Cache hit for {url}")
            data = cache[url]
        else:
            logging.info(f"Cache miss for {url}")
            if endHost is None:
                print("Host cannot be found in request")
                return

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.connect((endHost, endPort))
                server.sendall(request.encode())

                while True:
                    response = server.recv(4096)
                    if not response:
                        break
                    data += response

                cache[url] = data

        clientCon.send(data)

        duration = time.time() - timeStart
        print(f"Request processing duration: {duration:.4f} sec")

    except Exception as e:
        logging.error(f"Error in client connection: {e}")

    finally:
        clientCon.close()

def main():
    logging.basicConfig(level=logging.INFO)
    host = 'localhost'
    port = 9000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"Proxy server is running on {host}:{port}")

    try:
        while True:
            clientCon, client_addr = s.accept()
            thread = threading.Thread(target=connection, args=(clientCon,))
            thread.start()

    except KeyboardInterrupt:
        print("Server is shutting down.")

    finally:
        s.close()

if __name__ == '__main__':
    main()

