from pathlib import Path
from src.domains.customers.repository import CustomerRepository
from conf_test_seeds import ExpectedSeedData


def test_customer_spend_summaries_query(db_connection):
    repo = CustomerRepository(db_connection)
    summaries = repo.fetch_customer_spend_summaries()

    assert len(summaries) == ExpectedSeedData.EXPECTED_TOTAL_CUSTOMERS

    # Verify active VIP customer metrics
    alice = next(c for c in summaries if c.name == ExpectedSeedData.ALICE_NAME)
    assert alice.total_spend == ExpectedSeedData.ALICE_EXPECTED_SPEND
    assert alice.completed_orders_count == ExpectedSeedData.ALICE_EXPECTED_ORDERS
    assert alice.is_active is ExpectedSeedData.ALICE_EXPECTED_ACTIVE
    assert alice.segment == ExpectedSeedData.ALICE_EXPECTED_SEGMENT

    # Verify cancelled-order customer metrics
    charlie = next(c for c in summaries if c.name == ExpectedSeedData.CHARLIE_NAME)
    assert charlie.total_spend == ExpectedSeedData.CHARLIE_EXPECTED_SPEND
    assert charlie.is_active is ExpectedSeedData.CHARLIE_EXPECTED_ACTIVE
    assert charlie.segment == ExpectedSeedData.CHARLIE_EXPECTED_SEGMENT


def test_customers_with_no_orders(db_connection):
    repo = CustomerRepository(db_connection)
    never_ordered = repo.fetch_customers_with_no_orders()

    assert never_ordered == ExpectedSeedData.EXPECTED_NEVER_ORDERED