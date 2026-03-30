import threading
import time
import random
from queue import Queue

# ***================= GLOBAL DATA =================***
products = {}
carts = {}
orders = {}
logs = []
reservations = {}
event_queue = Queue()
lock = threading.Lock()
order_id_counter = 1
processed_requests = set()
user_orders_time = {}

# ================= LOGGING =================
def log(msg):
    logs.append(f"[{time.ctime()}] {msg}")

# ================= PRODUCT =================
def add_product():
    pid = input("Product ID: ")
    if pid in products:
        print("Duplicate ID ❌")
        return

    name = input("Name: ")
    stock = int(input("Stock: "))
    price = int(input("Price: "))

    if stock < 0:
        print("Invalid stock ❌")
        return

    products[pid] = {"name": name, "stock": stock, "price": price}
    log(f"Added product {pid}")
    print("Product added ✅")

def view_products():
    for pid, p in products.items():
        print(pid, p)

# ================= CART =================
def get_cart(user):
    if user not in carts:
        carts[user] = {}
    return carts[user]

def add_to_cart():
    user = input("User: ")
    pid = input("Product ID: ")
    qty = int(input("Qty: "))

    with lock:
        if pid not in products or products[pid]["stock"] < qty:
            print("Not enough stock ❌")
            return

        products[pid]["stock"] -= qty
        cart = get_cart(user)
        cart[pid] = cart.get(pid, 0) + qty

    log(f"{user} added {pid} qty={qty}")
    print("Added to cart ✅")

def remove_from_cart():
    user = input("User: ")
    pid = input("Product ID: ")

    cart = get_cart(user)
    if pid in cart:
        qty = cart[pid]
        products[pid]["stock"] += qty
        del cart[pid]

        log(f"{user} removed {pid}")
        print("Removed ✅")

def view_cart():
    user = input("User: ")
    print(get_cart(user))

# ================= DISCOUNT =================
def apply_discount(total, qty, coupon):
    if total > 1000:
        total *= 0.9
    if qty > 3:
        total *= 0.95
    if coupon == "SAVE10":
        total *= 0.9
    elif coupon == "FLAT200":
        total -= 200
    return max(total, 0)

#**** ================= FRAUD =================***
def check_fraud(user):
    now = time.time()
    user_orders_time.setdefault(user, []).append(now)

    recent = [t for t in user_orders_time[user] if now - t < 60]
    if len(recent) >= 3:
        print(" Fraud detected")

# ****================= ORDER =================****
def place_order():
    global order_id_counter

    user = input("User: ")
    request_id = input("Request ID: ")

    if request_id in processed_requests:
        print("Duplicate request ❌")
        return
    processed_requests.add(request_id)

    cart = get_cart(user)
    if not cart:
        print("Cart empty ❌")
        return

    total = 0
    total_qty = 0
    for pid, qty in cart.items():
        total += products[pid]["price"] * qty
        total_qty += qty

    coupon = input("Coupon (optional): ")
    total = apply_discount(total, total_qty, coupon)

    try:
        # FAILURE INJECTION
        if random.choice([False, True]):
            raise Exception("Random failure")

        # PAYMENT
        if random.choice([True, False]):
            order_id = order_id_counter
            order_id_counter += 1

            orders[order_id] = {
                "user": user,
                "items": cart.copy(),
                "total": total,
                "state": "PAID"
            }

            cart.clear()
            check_fraud(user)

            push_event("ORDER_CREATED")
            log(f"Order {order_id} created")

            print("Order Success ✅", order_id)

        else:
            raise Exception("Payment failed")

    except Exception as e:
        print("❌ Failed:", e)
        # ROLLBACK
        for pid, qty in cart.items():
            products[pid]["stock"] += qty
        log("Rollback executed")

# ================= ORDER MGMT =================
def view_orders():
    for oid, o in orders.items():
        print(oid, o)

def cancel_order():
    oid = int(input("Order ID: "))

    if oid not in orders:
        print("Invalid ID")
        return

    if orders[oid]["state"] == "CANCELLED":
        print("Already cancelled ❌")
        return

    for pid, qty in orders[oid]["items"].items():
        products[pid]["stock"] += qty

    orders[oid]["state"] = "CANCELLED"
    log(f"Order {oid} cancelled")
    print("Cancelled ")

# ================= RETURN =================
def return_product():
    oid = int(input("Order ID: "))
    pid = input("Product ID: ")
    qty = int(input("Qty: "))

    products[pid]["stock"] += qty
    orders[oid]["total"] -= qty * products[pid]["price"]

    log(f"Return processed {oid}")
    print("Return done")

#***================= INVENTORY =================***
def low_stock():
    for pid, p in products.items():
        if p["stock"] <= 5:
            print("Low stock:", pid)

#***================= EVENT SYSTEM =================***
def push_event(event):
    event_queue.put(event)

def process_events():
    while not event_queue.empty():
        print("Processing:", event_queue.get())

# ***================= LOG VIEW =================***
def view_logs():
    for l in logs:
        print(l)

# ***================= MENU =================***
def menu():
    while True:
        print("\n1.Add Product\n2.View Products\n3.Add to Cart\n4.Remove from Cart")
        print("5.View Cart\n6.Place Order\n7.Cancel Order\n8.View Orders")
        print("9.Low Stock\n10.Return\n11.View Logs\n12.Process Events\n0.Exit")

        ch = input("Choice: ")

        if ch == "1": add_product()
        elif ch == "2": view_products()
        elif ch == "3": add_to_cart()
        elif ch == "4": remove_from_cart()
        elif ch == "5": view_cart()
        elif ch == "6": place_order()
        elif ch == "7": cancel_order()
        elif ch == "8": view_orders()
        elif ch == "9": low_stock()
        elif ch == "10": return_product()
        elif ch == "11": view_logs()
        elif ch == "12": process_events()
        elif ch == "0": break

# ***================= RUN =================***
menu()