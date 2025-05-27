import asyncio
import aiohttp
import time
import json

async def single_request(session, url):
    start = time.time()
    async with session.get(url) as resp:
        data = await resp.json()
    duration = time.time() - start
    return duration, data['delay']

async def async_client(n=20, url='http://0.0.0.0:5000/delay'):
    result = {}
    start_all = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [single_request(session, url) for _ in range(n)]
        for duration, delay in await asyncio.gather(*tasks):
            result[duration] = delay
    total_time = time.time() - start_all

    return result, total_time

if __name__ == '__main__':
    n = 20
    server_delay_map, total = asyncio.run(async_client(n))

    output = {
        "AllRequestsTime": total,
        "ServerDelay": server_delay_map
    }
    with open("../results/result_async_asyncio.json", "w") as f:
        json.dump(output, f)