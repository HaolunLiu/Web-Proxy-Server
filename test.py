import requests
import time

def make_request_through_proxy(url, proxy):
    start_time = time.time()
    response = requests.get(url, proxies=proxy)
    duration = time.time() - start_time
    return response, duration

def main():
    proxy_url = 'http://localhost:9000'
    test_url = 'http://localhost:8000/test.html'  # Replace with the URL you want to test

    proxy = {
        'http': proxy_url,
        'https': proxy_url
    }

    # First request (likely cache miss)
    response1, duration1 = make_request_through_proxy(test_url, proxy)
    print(f"First request duration: {duration1:.4f} seconds")

    # Second request (likely cache hit)
    response2, duration2 = make_request_through_proxy(test_url, proxy)
    print(f"Second request duration: {duration2:.4f} seconds")
    response3, duration3 = make_request_through_proxy(test_url, proxy)
    print(f"Third request duration: {duration3:.4f} seconds")
    response4, duration4 = make_request_through_proxy(test_url, proxy)
    print(f"Fourth request duration: {duration4:.4f} seconds")
    response5, duration5 = make_request_through_proxy(test_url, proxy)
    print(f"Fifth request duration: {duration5:.4f} seconds")

    # Optionally, compare content of both responses
    if response1.content == response2.content:
        print("All responses have identical content.")
    else:
        print("The content of the responses differs.")

if __name__ == '__main__':
    main()
