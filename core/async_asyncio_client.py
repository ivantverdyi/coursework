import asyncio, aiohttp, time

async def single_request(session, url):
    t0 = time.time()
    async with session.get(url) as resp:
        data = await resp.json()
    return data['delay'], time.time() - t0

async def async_client(n=20, url='http://0.0.0.0:5000/delay'):
    t_start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [single_request(session, url) for _ in range(n)]
        results = await asyncio.gather(*tasks)
    delays, durations = zip(*results)
    return delays, durations, time.time() - t_start

if __name__ == '__main__':
    delays, durations, total = asyncio.run(async_client())
    print(delays, durations, total)
