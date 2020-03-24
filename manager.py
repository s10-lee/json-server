import asyncio
import time
from src.console import print_line

start = time.perf_counter()


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    begin = time.perf_counter()

    task1 = asyncio.create_task(say_after(1, 'First'))
    task2 = asyncio.create_task(say_after(2, 'Second'))
    task3 = asyncio.create_task(say_after(3, 'Third'))

    await task1
    await task2
    await task3

    print_line(f'Async <cyan>{round(time.perf_counter() - begin, 2)}</cyan>')
    asyncio.run(main())



