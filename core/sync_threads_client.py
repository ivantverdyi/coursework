import os
import time
import json
from concurrent.futures import ThreadPoolExecutor
from sync_client import single_request

def sync_threads_client(n=50, url='http://127.0.0.1:5000/delay', max_workers=4):
    output_dir = os.path.join(os.getcwd(), '../results')
    os.makedirs(output_dir, exist_ok=True)

    stats = {
        'individual_times': [],
        'server_delays': [],
        'count_success': 0,
        'count_failed': 0,
        'total_time': 0.0
    }

    start_all = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(single_request, url) for _ in range(n)]
        for i, fut in enumerate(futures, start=1):
            delay, rtt = fut.result()
            if delay is None or rtt is None:
                stats['count_failed'] += 1
            else:
                stats['count_success'] += 1
                stats['server_delays'].append(delay)
                stats['individual_times'].append(rtt)
                print(f"{i}: delay = {delay:.3f}s, round trip = {rtt:.3f}s")

    stats['total_time'] = time.perf_counter() - start_all
    return stats

if __name__ == '__main__':
    n = 100

    statistics = sync_threads_client(n=n)

    with open("../results/result_sync_threads.json", "w") as f:
        json.dump(statistics, f)