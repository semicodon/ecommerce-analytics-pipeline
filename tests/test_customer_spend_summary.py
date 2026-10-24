import csv
from pathlib import Path
from src.domains.customers.repository import CustomerRepository
from src.domains.analytics.reports import ReportGenerator
from tests.conf_test_seeds import ExpectedSeedData


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

    print(f'\n==== test_customer_spend_summaries_query ====')
    print(f'ALICE:')
    print(f'\t Total Spend: {alice.total_spend}')
    print(f'\t Completed Orders: {alice.completed_orders_count}')
    print(f'\t Active: {alice.is_active}')
    print(f'\t Segment: {alice.segment}')
    print(f'CHARLIE:')
    print(f'\t Total Spend: {charlie.total_spend}')
    print(f'\t Completed Orders: {charlie.completed_orders_count}')
    print(f'\t Active: {charlie.is_active}')
    print(f'\t Segment: {charlie.segment}')


def test_customers_with_no_orders(db_connection):
    repo = CustomerRepository(db_connection)
    never_ordered = repo.fetch_customers_with_no_orders()

    assert never_ordered == ExpectedSeedData.EXPECTED_NEVER_ORDERED

def test_customer_window_metrics_view(db_connection):
    repo = CustomerRepository(db_connection)
    metrics = repo.fetch_customer_window_metrics()

    assert len(metrics) == ExpectedSeedData.EXPECTED_TOTAL_CUSTOMERS

    alice = next(m for m in metrics if m.name == ExpectedSeedData.ALICE_NAME)
    assert alice.spend_rank == ExpectedSeedData.ALICE_EXPECTED_RANK
    assert alice.global_revenue_share_pct == ExpectedSeedData.ALICE_EXPECTED_GLOBAL_SHARE
    assert alice.country_revenue_share_pct == ExpectedSeedData.ALICE_EXPECTED_COUNTRY_SHARE

    diana = next(m for m in metrics if m.name == ExpectedSeedData.DIANA_NAME)
    assert diana.spend_rank == ExpectedSeedData.DIANA_EXPECTED_RANK
    assert diana.global_revenue_share_pct == ExpectedSeedData.DIANA_EXPECTED_GLOBAL_SHARE

    # Verify DENSE_RANK ties $0.00 customers at rank 4
    charlie = next(m for m in metrics if m.name == ExpectedSeedData.CHARLIE_NAME)
    assert charlie.spend_rank == ExpectedSeedData.CHARLIE_EXPECTED_RANK
    assert charlie.global_revenue_share_pct == ExpectedSeedData.CHARLIE_EXPECTED_GLOBAL_SHARE

    print(f'\n==== test_customer_spend_summary: customer_window_metrics_view ====')
    print(f'ALICE:')
    print(f'\tSpend Rank: {alice.spend_rank}')
    print(f'\tGlobal Revenue Share: {alice.global_revenue_share_pct}')
    print(f'\tCountry Revenue Share: {alice.country_revenue_share_pct}')
    print(f'DIANA:')
    print(f'\tSpend Rank: {diana.spend_rank}')
    print(f'\tGlobal Revenue Share: {diana.global_revenue_share_pct}')
    print(f'\tCountry Revenue Share: {diana.country_revenue_share_pct}')
    print(f'CHARLIE:')
    print(f'\tSpend Rank: {charlie.spend_rank}')
    print(f'\tGlobal Revenue Share: {charlie.global_revenue_share_pct}')
    print(f'\tCountry Revenue Share: {charlie.country_revenue_share_pct}')


def test_export_kpi_mart_csv(db_connection, tmp_path: Path):
    repo = CustomerRepository(db_connection)
    metrics = repo.fetch_customer_window_metrics()

    csv_file = ReportGenerator.export_kpi_mart_csv(
        metrics,
        output_dir=tmp_path)
    assert csv_file.exists()

    with csv_file.open(mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == ExpectedSeedData.EXPECTED_TOTAL_CUSTOMERS
    assert rows[0]["name"] == ExpectedSeedData.ALICE_NAME
    assert rows[0]["spend_rank"] == "1"
    assert rows[0]["global_revenue_share_pct"] == "82.71"

    print(f'\n==== test_customer_spend_summary: export_kpi_mart_csv ====')
    print(f'Exported CSV file: {csv_file}')
    print(f'First row: {rows[0]}')
    print(f'Last row: {rows[-1]}')

