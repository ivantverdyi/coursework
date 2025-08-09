import os
import requests
import time
import json

def single_request(url):
    try:
        start_time = time.perf_counter()
        response = requests.get(url)
        data = response.json()
        end_time = time.perf_counter()

        return data['delay'], end_time - start_time
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None, None

def sync_client(n=50, url='http://127.0.0.1:5000/delay'):

    output_dir = os.path.join(os.getcwd(), '../results')
    os.makedirs(output_dir, exist_ok=True)

    stats = {
        'individual_times': [],
        'server_delays': [],
        'count_success': 0,
        'count_failed': 0,
        'total_time': 0.0,
    }

    total_start = time.perf_counter()

    for i in range(1, n + 1):
        delay, rtt = single_request(url)
        if delay is None or rtt is None:
            stats['count_failed'] += 1
            continue

        stats['individual_times'].append(rtt)
        stats['server_delays'].append(delay)
        stats['count_success'] += 1
        print(f"{i}: delay = {delay:.3f}s, round trip of 1 request = {rtt:.3f}s")

    total_time = time.perf_counter() - total_start
    stats['total_time'] = total_time

    return stats

if __name__ == '__main__':
    n = 100
    statistics = sync_client(n)

    with open("../results/result_sync.json", "w") as f:
        json.dump(statistics, f)