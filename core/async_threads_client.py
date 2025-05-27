import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor
from sync_client import single_request

def async_client(n=20, url='http://0.0.0.0:5000/delay', max_workers=4):
    result = {}
    start_all = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(single_request, url) for _ in range(n)]
        for fut in futures:
            duration, delay = fut.result()
            result[delay] = duration
    total_time = time.time() - start_all

    return result, total_time

if __name__ == '__main__':
    n = 20
    server_delay_map, total = async_client(n=n)

    output = {
        "AllRequestsTime": total,
        "ServerDelay": server_delay_map
    }
    with open("../results/result_async_threads.json", "w") as f:
        json.dump(output, f)