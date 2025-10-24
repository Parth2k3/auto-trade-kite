import asyncio, httpx, time
from datetime import datetime, timedelta

API_KEY = "u82kuvexq39lq7hk"
ACCESS_TOKEN = "DNGyn4YglG6YULOmF307zD2dINsOjTcV"

# Create an async client once and reuse it
client = httpx.AsyncClient(
    base_url="https://api.kite.trade",
    headers={
        "X-Kite-Version": "3",
        "Authorization": f"token {API_KEY}:{ACCESS_TOKEN}"
    },
    timeout=2.0
)

async def place_order():
    data = {
        "exchange": "BSE",
        "tradingsymbol": "AVANCE",
        "transaction_type": "SELL",
        "order_type": "LIMIT",
        "price": 2.67,
        "quantity": 20062,
        "product": "CNC",
        "variety": "regular"
    }
    r = await client.post("/orders/regular", data=data)
    print(datetime.now(), "Response:", r.text)

async def wait_and_fire(target):
    # warm up connection
    await client.get("/orders")
    print("Waiting for", target)
    while datetime.now() < target - timedelta(milliseconds=150):
        await asyncio.sleep(0.002)
    while datetime.now() < target:
        pass
    await place_order()

target = datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
asyncio.run(wait_and_fire(target))
