import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor

def single_request(url):
    start_time = time.time()
    response = requests.get(url)
    resp = json.loads(response.text)
    end_time = time.time()
    return resp, end_time - start_time

def async_client(n=20, url='http://0.0.0.0:5000/delay'):
    with ThreadPoolExecutor(max_workers=n) as executor:
        futures = [executor.submit(single_request, url) for _ in range(n)]


        for i in futures:
            r, duration = i.result()
            print(r, duration)


async_client()