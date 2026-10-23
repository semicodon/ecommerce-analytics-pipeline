from pathlib import Path
from src.domains.customers.repository import CustomerRepository

def test_customer_spend_summaries_query(db_connection):
    repo = CustomerRepository(db_connection)
    summaries = repo.fetch_customer_spend_summaries()

    assert len(summaries) == 5

    # Alice (id=1): 1x120 + 2x15 + 1x400 = $550.00 across 2 completed orders
    alice = next(c for c in summaries if c.name == "Alice Johnson")
    assert alice.total_spend == 550.0
    assert alice.completed_orders_count == 2
    assert alice.is_active is True
    assert alice.segment == "VIP"

    # Charlie (id=3) only has a CANCELLED order -> $0 completed spend
    charlie = next(c for c in summaries if c.name == "Charlie Brown")
    assert charlie.total_spend == 0.0
    assert charlie.is_active is False
    assert charlie.segment == "Inactive"

def test_customers_with_no_orders(db_connection):
    repo = CustomerRepository(db_connection)
    never_ordered = repo.fetch_customers_with_no_orders()

    assert never_ordered == ["Evan Wright"]