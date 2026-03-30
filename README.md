# Kousalya_Ecommerce_Order_Engine_Hackathon
CLI-based E-commerce Order Engine simulating real backend systems. Supports product &amp; inventory management, multi-user carts, order processing, payment handling, rollback, concurrency control, fraud detection, logging, and event-driven operations ensuring consistency and scalability.
# 🛒 E-Commerce Order Engine (Hackathon Project)

## 📌 Project Overview

This project is a **CLI-based Distributed E-Commerce Order Engine** that simulates real-world backend operations of platforms like Amazon and Flipkart.

The system is designed to handle:

* Multiple users
* Inventory management
* Order processing
* Payment failures
* Concurrency issues
* Transaction rollback
* Event-driven processing

It ensures **data consistency, scalability simulation, and fault tolerance**.

---

## 🚀 Features Implemented

### ✅ Product Management

* Add new products
* Prevent duplicate product IDs
* Update and view inventory
* Stock validation (no negative values)

### ✅ Multi-User Cart System

* Separate cart for each user
* Add/remove/update items
* Real-time stock synchronization

### ✅ Stock Reservation System

* Stock reserved when added to cart
* Released when removed or order fails
* Prevents overselling

### ✅ Concurrency Handling

* Implemented locking mechanism
* Ensures only one user can modify stock at a time

### ✅ Order Placement Engine

* Converts cart → order
* Calculates total cost
* Atomic operation (all or nothing)

### ✅ Payment Simulation

* Random success/failure simulation
* Handles retry scenarios

### ✅ Transaction Rollback System

* If any step fails:

  * Restore stock
  * Cancel order
* Ensures system consistency

### ✅ Order State Machine

Supported states:

* CREATED
* PENDING_PAYMENT
* PAID
* SHIPPED
* DELIVERED
* FAILED
* CANCELLED

Invalid transitions are blocked.

### ✅ Discount & Coupon Engine

* 10% discount for orders > ₹1000
* 5% extra discount for quantity > 3
* Coupons:

  * SAVE10 → 10% off
  * FLAT200 → ₹200 off

### ✅ Inventory Alert System

* Alerts for low stock
* Prevents purchase if stock = 0

### ✅ Order Management

* View all orders
* Search by order ID
* Filter by status

### ✅ Order Cancellation

* Cancel order
* Restore stock
* Prevent duplicate cancellation

### ✅ Return & Refund System

* Partial return supported
* Updates stock and order total

### ✅ Event-Driven System

* Event queue implementation
* Events executed sequentially
* Stops execution on failure

### ✅ Inventory Reservation Expiry

* Reserved stock auto-released after timeout

### ✅ Audit Logging System

* Immutable logs maintained
* Tracks all actions with timestamps

### ✅ Fraud Detection

* Flags user if:

  * 3 orders within 1 minute
  * High-value transactions

### ✅ Failure Injection System

* Random failure simulation:

  * Payment
  * Order creation
  * Inventory update

### ✅ Idempotency Handling

* Prevents duplicate orders on repeated clicks

### ✅ Microservice Simulation

System divided into logical modules:

* Product Service
* Cart Service
* Order Service
* Payment Service

---

## 🧠 Design Approach

* Implemented using **modular programming**
* Used **Python dictionaries** as in-memory database
* Applied **locking (threading.Lock)** for concurrency control
* Designed **transaction system with rollback mechanism**
* Implemented **event queue** for asynchronous simulation
* Maintained **clean separation of concerns** (microservice-like)

---

## 📌 Assumptions

* Data is stored in-memory (no database used)
* CLI-based interaction (no UI)
* Payment gateway is simulated
* Concurrency is simulated using threading
* Inventory expiry is time-based (simplified)

---

## ▶️ How to Run the Project

1. Install Python (if not installed)

2. Clone the repository:

```
git clone <your-repo-link>
```

3. Navigate to project folder:

```
cd <your-repo-name>
```

4. Run the application:

```
python main.py
```

---

## 🖥️ Sample Menu

```
1. Add Product
2. View Products
3. Add to Cart
4. Remove from Cart
5. View Cart
6. Apply Coupon
7. Place Order
8. Cancel Order
9. View Orders
10. Low Stock Alert
11. Return Product
12. Simulate Concurrent Users
13. View Logs
14. Trigger Failure Mode
0. Exit
```

---

## 📊 Key Highlights

* Prevents overselling using stock reservation
* Ensures data consistency via rollback
* Simulates real-world backend failures
* Handles concurrency using locks
* Implements complete order lifecycle

---

## 🔗 Submission

GitHub Repository Link:
👉 *Add your repository URL here*

---

## 👩‍💻 Author

Rupasri Gopidesi
