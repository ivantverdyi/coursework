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
    t = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(single_request, url) for _ in range(n)]

        res = []
        times = []
        for i in futures:
            r, duration = i.result()
            res.append(r['delay'])
            times.append(duration)
    end = time.time()
    async_time = end - t
    return res, times, async_time


if __name__ == '__main__':
    n = 20
    res, times, async_time = async_client(n=n, url='http://0.0.0.0:5000/delay')
    print("=" * 30)
    print(times)
    print(res)
    print(async_time)

    result = {"SyncResp": res, "SyncRes": times}
    with open("../results/result_async_threads.json", "w") as f:
        json.dump(result, f)