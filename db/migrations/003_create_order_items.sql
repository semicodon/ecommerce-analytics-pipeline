CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price REAL NOT NULL CHECK (price >= 0),
    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE
    );