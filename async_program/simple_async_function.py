import asyncio

async def simple_async_function():
    print("Hello from the async function!")
    await asyncio.sleep(1)
    print("Async function has finished executing!")
    
asyncio.run(simple_async_function())


async def task1():
    print("Task 1 starting...")
    await asyncio.sleep(2)
    print("Task 1 completed!")
    
async def task2():
    print("Task 2 starting...")
    await asyncio.sleep(1)
    print("Task 2 completed!")
    
async def main():
    print("Main function starting...")
    await asyncio.gather(task1(), task2())
    print("Main function completed!")
    
asyncio.run(main())




async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)
    print("Data fetched!")
    return {"name": "John", "age": 30}

async def process_data(data):
    print(f"Processing data: {data}")
    await asyncio.sleep(1)
    print("Data processed!")
    return {"status": "success"}

async def main():
    task1 = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(process_data({"name": "Alby", "age": 28}))
    await asyncio.gather(task1, task2)
    
    data = await task1
    print(f"Received data: {data}")
    
    await task2
    print("All tasks completed!")
    
asyncio.run(main())


async def run_function():
    print("Running async function...")
    async def print_hello():
        await asyncio.sleep(2)
        print("Hello from the inner async function!")
    
    await print_hello()
    print("Async function completed!")
    
asyncio.run(run_function())