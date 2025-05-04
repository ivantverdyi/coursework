import requests
import time
import json

def sync_client(n, url='http://0.0.0.0:5000/delay'):
    num_of_times = []
    resp = []
    for _ in range(n):
        start = time.time()
        raw_resp = requests.get(url)
        resp.append(json.loads(raw_resp.text)['delay'])
        end = time.time()
        num_of_times.append(end - start)
    return resp, num_of_times

if __name__ == '__main__':
    n = 20
    resp, times = sync_client(n)
    print("=" * 30)
    print(times)
    print(resp)
    res = {"SyncResp": resp, "SyncRes": times}
    with open("../results/result_sync.json", "w") as f:
        json.dump(res, f)