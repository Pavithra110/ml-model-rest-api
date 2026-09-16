import asyncio
import os
import time

import httpx


URL = "http://127.0.0.1:8000/api/v1/predict"
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set.")

TOTAL_REQUESTS = 100


inputs = [
    {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    },
    {
        "sepal_length": 6.0,
        "sepal_width": 2.9,
        "petal_length": 4.5,
        "petal_width": 1.5,
    },
    {
        "sepal_length": 6.5,
        "sepal_width": 3.0,
        "petal_length": 5.2,
        "petal_width": 2.0,
    },
]


async def send_request(client, payload):
    start = time.perf_counter()

    try:
        response = await client.post(
            URL,
            headers={"X-API-Key": API_KEY},
            json=payload,
        )

        duration = time.perf_counter() - start

        return response.status_code, duration

    except Exception as exc:
        duration = time.perf_counter() - start
        return f"ERROR: {exc}", duration


async def main():
    async with httpx.AsyncClient(timeout=10.0) as client:

        tasks = [
            send_request(client, inputs[i % len(inputs)])
            for i in range(TOTAL_REQUESTS)
        ]

        start = time.perf_counter()

        results = await asyncio.gather(*tasks)

        total_duration = time.perf_counter() - start

    successful = [
        duration
        for status, duration in results
        if status == 200
    ]

    failed = [
        (status, duration)
        for status, duration in results
        if status != 200
    ]

    print("\n--- Load Test Results ---")
    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Total test duration: {total_duration:.4f} seconds")

    if successful:
        print(
            f"Average response time: "
            f"{sum(successful) / len(successful):.4f} seconds"
        )
        print(f"Fastest response: {min(successful):.4f} seconds")
        print(f"Slowest response: {max(successful):.4f} seconds")

    if failed:
        print("\nFailed requests:")
        for status, duration in failed:
            print(f"  {status} - {duration:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main())