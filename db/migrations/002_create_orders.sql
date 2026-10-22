CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('PENDING', 'COMPLETED', 'CANCELLED')),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE
    );