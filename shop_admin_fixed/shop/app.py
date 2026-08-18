from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = "stationery-shop-secret-key"
DB = "shop.db"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"
LOW_STOCK_LIMIT = 5


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER DEFAULT 0,
            description TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        products = [
            ("Class Notebook", "Stationery", 45, 100, "200-page ruled notebook"),
            ("Blue Pen", "Stationery", 10, 250, "Smooth writing blue ball pen"),
            ("Geometry Box", "Stationery", 120, 50, "Complete geometry set"),
            ("School Shirt", "School Dress", 550, 30, "White school uniform shirt"),
            ("School Pant", "School Dress", 650, 25, "Navy blue school uniform pant"),
            ("School Tie", "School Dress", 150, 40, "Official school uniform tie"),
            ("School Belt", "School Dress", 180, 35, "Black school belt"),
            ("School Shoes", "School Dress", 850, 20, "Black school shoes"),
        ]
        conn.executemany(
            "INSERT INTO products (name, category, price, stock, description) VALUES (?, ?, ?, ?, ?)",
            products
        )
    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db()
    products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("index.html", products=products)


@app.route("/products")
def products():
    category = request.args.get("category", "All")
    conn = get_db()
    if category in ["Stationery", "School Dress"]:
        items = conn.execute(
            "SELECT * FROM products WHERE category=? ORDER BY name", (category,)
        ).fetchall()
    else:
        items = conn.execute("SELECT * FROM products ORDER BY name").fetchall()
    conn.close()
    return render_template("products.html", products=items, category=category)


@app.route("/order", methods=["POST"])
def order():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    product_id = request.form.get("product_id")

    if not name or not phone or not product_id:
        flash("Please fill all required details.")
        return redirect(url_for("home"))

    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()

    if not product:
        flash("Product not found.")
    elif product["stock"] <= 0:
        flash("Sorry, this product is out of stock.")
    else:
        conn.execute("UPDATE products SET stock = stock - 1 WHERE id=?", (product_id,))
        conn.execute("""
            INSERT INTO orders (customer_name, phone, product_id, product_name, price, status)
            VALUES (?, ?, ?, ?, ?, 'Pending')
        """, (name, phone, product_id, product["name"], product["price"]))
        conn.commit()
        flash(f"Order request received for {product['name']}. We will contact you at {phone}.")
    conn.close()
    return redirect(url_for("home"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    conn = get_db()
    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    low_stock = conn.execute(
        "SELECT COUNT(*) FROM products WHERE stock <= ?", (LOW_STOCK_LIMIT,)
    ).fetchone()[0]
    total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    pending_orders = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE status='Pending'"
    ).fetchone()[0]
    completed_orders = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE status='Completed'"
    ).fetchone()[0]
    cancelled_orders = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE status='Cancelled'"
    ).fetchone()[0]
    recent_orders = conn.execute(
        "SELECT * FROM orders ORDER BY id DESC LIMIT 5"
    ).fetchall()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_products=total_products,
        low_stock=low_stock,
        total_orders=total_orders,
        pending_orders=pending_orders,
        completed_orders=completed_orders,
        cancelled_orders=cancelled_orders,
        recent_orders=recent_orders,
    )


@app.route("/admin/add", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category")
        price = request.form.get("price")
        stock = request.form.get("stock")
        description = request.form.get("description", "").strip()

        if not name or not price or not stock:
            flash("Name, price and stock are required.")
            return redirect(url_for("add_product"))

        try:
            price_value = float(price)
            stock_value = int(stock)
            if price_value < 0 or stock_value < 0:
                raise ValueError
        except ValueError:
            flash("Price and stock must contain valid positive values.")
            return redirect(url_for("add_product"))

        conn = get_db()
        conn.execute(
            "INSERT INTO products (name, category, price, stock, description) VALUES (?, ?, ?, ?, ?)",
            (name, category, price_value, stock_value, description)
        )
        conn.commit()
        conn.close()
        flash("Product added successfully.")
        return redirect(url_for("admin_products"))

    return render_template("add_product.html")


@app.route("/admin/products")
@admin_required
def admin_products():
    conn = get_db()
    products = conn.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin_products.html", products=products, low_stock_limit=LOW_STOCK_LIMIT)


@app.route("/admin/edit/<int:product_id>", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()

    if not product:
        conn.close()
        flash("Product not found.")
        return redirect(url_for("admin_products"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        category = request.form.get("category")
        price = request.form.get("price")
        stock = request.form.get("stock")
        description = request.form.get("description", "").strip()

        try:
            price_value = float(price)
            stock_value = int(stock)
            if not name or price_value < 0 or stock_value < 0:
                raise ValueError
        except (ValueError, TypeError):
            flash("Please enter valid product details.")
            conn.close()
            return redirect(url_for("edit_product", product_id=product_id))

        conn.execute("""
            UPDATE products
            SET name=?, category=?, price=?, stock=?, description=?
            WHERE id=?
        """, (name, category, price_value, stock_value, description, product_id))
        conn.commit()
        conn.close()
        flash("Product updated successfully.")
        return redirect(url_for("admin_products"))

    conn.close()
    return render_template("edit_product.html", product=product)


@app.route("/admin/delete/<int:product_id>", methods=["POST"])
@admin_required
def delete_product(product_id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()

    if not product:
        conn.close()
        flash("Product not found.")
        return redirect(url_for("admin_products"))

    existing_orders = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE product_id=?", (product_id,)
    ).fetchone()[0]

    if existing_orders:
        conn.close()
        flash("This product has customer orders and cannot be deleted. You can set its stock to 0 instead.")
        return redirect(url_for("admin_products"))

    conn.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    flash("Product deleted successfully.")
    return redirect(url_for("admin_products"))


@app.route("/admin/orders")
@admin_required
def admin_orders():
    status = request.args.get("status", "All")
    conn = get_db()
    if status in ["Pending", "Confirmed", "Completed", "Cancelled"]:
        orders = conn.execute(
            "SELECT * FROM orders WHERE status=? ORDER BY id DESC", (status,)
        ).fetchall()
    else:
        orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin_orders.html", orders=orders, status=status)


@app.route("/admin/orders/<int:order_id>/status", methods=["POST"])
@admin_required
def update_order_status(order_id):
    new_status = request.form.get("status")
    valid_statuses = {"Pending", "Confirmed", "Completed", "Cancelled"}
    if new_status not in valid_statuses:
        flash("Invalid order status.")
        return redirect(url_for("admin_orders"))

    conn = get_db()
    order_row = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    if not order_row:
        conn.close()
        flash("Order not found.")
        return redirect(url_for("admin_orders"))

    old_status = order_row["status"]

    # Stock was reduced when the order was placed. Restore it when an order is cancelled.
    if old_status != "Cancelled" and new_status == "Cancelled":
        conn.execute("UPDATE products SET stock = stock + 1 WHERE id=?", (order_row["product_id"],))
    elif old_status == "Cancelled" and new_status != "Cancelled":
        product = conn.execute("SELECT stock FROM products WHERE id=?", (order_row["product_id"],)).fetchone()
        if product and product["stock"] <= 0:
            conn.close()
            flash("Cannot reopen this cancelled order because the product is out of stock.")
            return redirect(url_for("admin_orders"))
        conn.execute("UPDATE products SET stock = stock - 1 WHERE id=?", (order_row["product_id"],))

    conn.execute("UPDATE orders SET status=? WHERE id=?", (new_status, order_id))
    conn.commit()
    conn.close()
    flash(f"Order #{order_id} status updated to {new_status}.")
    return redirect(url_for("admin_orders"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
