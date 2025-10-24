from kiteconnect import KiteConnect
import time
from datetime import datetime, timedelta
import threading

kite_api_key = "u82kuvexq39lq7hk"
kite_access_token = "E3swu2C8h0a9NbpWxN3FpVa24tHFVdGC"  # fetched from your Flask app

kite = KiteConnect(api_key=kite_api_key)
kite.set_access_token(kite_access_token)

ttpo = "09:30:00"

def place_order():
    try:
        order_id = kite.place_order(
            variety=kite.VARIETY_REGULAR,
            exchange=kite.EXCHANGE_BSE,
            tradingsymbol="ATLANTAELE",
            transaction_type=kite.TRANSACTION_TYPE_SELL,
            quantity=1,
            order_type=kite.ORDER_TYPE_LIMIT,
            price=1110.05,
            product=kite.PRODUCT_CNC
        )
        print(f"✅ Order placed successfully! ID: {order_id} ", datetime.now())
    except Exception as e:
        print("❌ Error:", e)

# def run_at(target_time_str):
#     target_time = datetime.strptime(target_time_str, "%H:%M:%S").time()
#     kite.orders()  # lightweight API call to warm up HTTPS session

#     while True:
#         while datetime.now() < target_time - timedelta(milliseconds=200):
#             time.sleep(0.05)  # coarse waiting
#     # Busy wait for last 200 ms
#         while datetime.now() < target_time:
#             pass
#         if datetime.now().time() >= target_time:
#             print(datetime.now())
#             place_order()
#             print(datetime.now())
#             break
#         print('waiting ', datetime.now())
#         time.sleep(0.00000000000001)

# run_at(ttpo)

def wait_and_fire(target_time):
    kite.orders()  # prewarm HTTPS
    print("Waiting for", target_time)
    while datetime.now() < target_time - timedelta(milliseconds=200):
        time.sleep(0.005)
    while datetime.now() < target_time:
        pass
    threading.Thread(target=place_order).start()

target_time = datetime.now().replace(hour=15, minute=12, second=0, microsecond=0)
wait_and_fire(target_time)
