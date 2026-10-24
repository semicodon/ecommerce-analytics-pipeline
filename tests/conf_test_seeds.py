SEED_CUSTOMERS = """
    INSERT OR IGNORE INTO customers (customer_id, name, country, signup_date) VALUES
    (1, 'Alice Johnson', 'USA', '2023-01-15'),
    (2, 'Bob Smith', 'Canada', '2023-02-10'),
    (3, 'Charlie Brown', 'USA', '2023-03-05'),
    (4, 'Diana Prince', 'UK', '2023-04-12'),
    (5, 'Evan Wright', 'Canada', '2023-05-20');
"""

SEED_ORDERS = """
    INSERT OR IGNORE INTO orders (order_id, customer_id, order_date, status) VALUES
    (101, 1, '2023-06-01', 'COMPLETED'),
    (102, 1, '2023-08-15', 'COMPLETED'),
    (103, 2, '2023-07-20', 'COMPLETED'),
    (104, 3, '2023-04-10', 'CANCELLED'),
    (105, 4, '2023-09-01', 'COMPLETED');
"""

SEED_ORDER_ITEMS = """
    INSERT OR IGNORE INTO order_items (item_id, order_id, product_name, quantity, price) VALUES
    (1, 101, 'Mechanical Keyboard', 1, 120.00),
    (2, 101, 'USB-C Cable', 2, 15.00),
    (3, 102, '4K Monitor', 1, 400.00),
    (4, 103, 'Wireless Mouse', 1, 50.00),
    (5, 105, 'Laptop Stand', 1, 65.00);
"""

# Centralized Expected Baseline Metrics
class ExpectedSeedData:
    EXPECTED_TOTAL_CUSTOMERS = 5
    EXPECTED_ACTIVE_CUSTOMERS = 3
    EXPECTED_CHURNED_CUSTOMERS = 2
    EXPECTED_TOTAL_REVENUE = 665.0
    EXPECTED_ARPU = round(665.0 / 3, 2)

    # --- Customer Spend Summary Expectations (used by test_customer_spend_summary.py) ---
    ALICE_NAME = "Alice Johnson"
    ALICE_EXPECTED_SPEND = 550.0
    ALICE_EXPECTED_ORDERS = 2
    ALICE_EXPECTED_ACTIVE = True
    ALICE_EXPECTED_SEGMENT = "VIP"

    CHARLIE_NAME = "Charlie Brown"
    CHARLIE_EXPECTED_SPEND = 0.0
    CHARLIE_EXPECTED_ACTIVE = False
    CHARLIE_EXPECTED_SEGMENT = "Inactive"

    EXPECTED_NEVER_ORDERED = ["Evan Wright"]

    # --- Window Function & Revenue Share Expectations ---
    ALICE_EXPECTED_RANK = 1
    ALICE_EXPECTED_GLOBAL_SHARE = 82.71  # 550.0 / 665.0 * 100
    ALICE_EXPECTED_COUNTRY_SHARE = 100.0  # 550.0 / 550.0 (USA total) * 100

    DIANA_NAME = "Diana Prince"
    DIANA_EXPECTED_RANK = 2
    DIANA_EXPECTED_GLOBAL_SHARE = 9.77   # 65.0 / 665.0 * 100

    CHARLIE_EXPECTED_RANK = 4            # Tied at $0.00 with Evan Wright
    CHARLIE_EXPECTED_GLOBAL_SHARE = 0.0