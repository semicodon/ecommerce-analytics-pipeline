
INSERT INTO customers (customer_id, name, country, signup_date)
VALUES
    (1, 'Alice Johnson', 'USA', '2023-01-15'),
    (2, 'Bob Smith', 'Canada', '2023-02-10'),
    (3, 'Charlie Brown', 'USA', '2023-03-05'),
    (4, 'Diana Prince', 'UK', '2023-04-12'),
    (5, 'Evan Wright', 'Canada', '2023-05-20');

INSERT INTO orders (order_id, customer_id, order_id, status)
VALUES
    (101, 1, '2023-06-01', 'COMPLETED'),
    (102, 1, '2023-08-15', 'COMPLETED'),
    (103, 2, '2023-07-20', 'COMPLETED'),
    (104, 3, '2023-04-10', 'CANCELLED'),
    (105, 4, '2023-09-01', 'COMPLETED');

INSERT INTO order_items(item_id, order_id, product_name, quantity, price)
VALUES
    (1, 101, 'Mechanical Keyboard', 1, 120.00),
    (2, 101, 'USB-C Cable', 2, 15.00),
    (3, 102, '4K Monitor', 1, 400.00),
    (4, 103, 'Wireless Mouse', 1, 50.00),
    (5, 105, 'Laptop Stand', 1, 65.00);