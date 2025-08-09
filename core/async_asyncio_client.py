import os
import json
import time
import asyncio
import aiohttp

async def single_request(session, url):
    try:
        start = time.perf_counter()
        async with session.get(url) as resp:
            data = await resp.json()
        elapsed = time.perf_counter() - start
        return data['delay'], elapsed
    except Exception as e:
        print(f"Request failed: {e}")
        return None, None

async def async_asyncio_client(n=50, url='http://127.0.0.1:5000/delay'):
    output_dir = os.path.join(os.getcwd(), '../results')
    os.makedirs(output_dir, exist_ok=True)

    stats = {
        'individual_times': [],
        'server_delays': [],
        'count_success': 0,
        'count_failed': 0,
        'total_time': 0.0
    }

    async with aiohttp.ClientSession() as session:
        start_all = time.perf_counter()
        tasks = [single_request(session, url) for _ in range(n)]
        results = await asyncio.gather(*tasks)
        for i, (delay, rtt) in enumerate(results, start=1):
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
    statistics = asyncio.run(async_asyncio_client(n))

    with open("../results/result_async_asyncio.json", "w") as f:
        json.dump(statistics, f)