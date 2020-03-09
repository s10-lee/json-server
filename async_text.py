import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def main():
    print(f'Start: {time.strftime("%X")}')

    task1 = asyncio.create_task(
        say_after(2, 'Hello'))

    task2 = asyncio.create_task(
        say_after(3, 'World'))

    await task1
    await task2

    print(f'Finish: {time.strftime("%X")}')

asyncio.run(main())
