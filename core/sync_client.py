import requests
import time
import json

def single_request(url):
    start_time = time.time()
    response = requests.get(url)
    resp = json.loads(response.text)
    end_time = time.time()
    return resp['delay'], end_time - start_time

def sync_client(n, url='http://0.0.0.0:5000/delay'):
    result = {}
    start = time.time()
    for _ in range(n):
        delay, req_time = single_request(url)
        result[req_time] = delay

    return result, time.time() - start

if __name__ == '__main__':
    n = 20
    server_delay_map, total = sync_client(n)

    output = {
        "AllRequestsTime": total,
        "ServerDelay": server_delay_map
    }
    with open("../results/result_sync.json", "w") as f:
        json.dump(output, f)