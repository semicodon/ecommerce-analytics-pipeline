import sqlite3
from typing import List
from src.domains.customers.entity import CustomerSpendSummary

class CustomerRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def fetch_customer_spend_summaries(self) -> List[CustomerSpendSummary]:
        """Executes analytical aggregation joining customers, orders, and line items."""

        query = """
                SELECT
                    c.customer_id,
                    c.name,
                    c.country,
                    COUNT(DISTINCT o.order_id) AS completed_orders_count,
                    COALESCE(SUM(oi.quantity * oi.price), 0.0) AS total_spend,
                    MAX(o.order_date) AS last_order_date
                FROM customers c
                         LEFT JOIN orders o
                                   ON c.customer_id = o.customer_id
                                       AND o.status = 'COMPLETED'
                         LEFT JOIN order_items oi
                                   ON o.order_id = oi.order_id
                GROUP BY c.customer_id, c.name, c.country
                ORDER BY total_spend DESC, c.customer_id ASC;
                    
                """
        rows = self.conn.execute(query).fetchall()

        return [
            CustomerSpendSummary(
                customer_id=row['customer_id'],
                name=row['name'],
                country=row['country'],
                completed_orders_count=row['completed_orders_count'],
                total_spend=row['total_spend'],
                last_order_date=row['last_order_date'],
            )
        for row in rows
        ]


    def fetch_customers_with_no_orders(self) -> List[str]:
        """Finds customers who have never placed any order (even cancelled ones)."""

        query = """
            SELECT c.name
            FROM customers c
            LEFT JOIN orders o 
                ON c.customer_id = o.customer_id
                WHERE o.order_id is NULL
            ORDER BY c.name ASC;
        """

        rows = self.conn.execute(query).fetchall()
        return [
            row['name']
            for row in rows
        ]