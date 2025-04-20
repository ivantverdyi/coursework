import requests
import time
import json

def sync_client(n):
    num_of_times = []
    for _ in range(n):
        start = time.time()
        raw_resp = requests.get('http://0.0.0.0:5000/delay')
        resp = json.loads(raw_resp.text)
        print(resp)
        end = time.time()
        num_of_times.append(end - start)
    return num_of_times

if __name__ == '__main__':
    n = 20
    times = sync_client(n)
    print("="*30)
    print(times)