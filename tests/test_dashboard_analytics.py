from src.domains.customers.repository import CustomerRepository
from src.domains.analytics.service import AnalyticsService
from tests.conf_test_seeds import ExpectedSeedData


def test_dashboard_slice_country_filter(db_connection):
    repo = CustomerRepository(db_connection)
    service = AnalyticsService(repo)

    # Filter strictly to USA (Alice: $550.00 active, Charlie: $0.00 inactive)
    usa_slice = service.generate_dashboard_slice(countries=["USA"])

    assert usa_slice.total_customers == 2
    assert usa_slice.active_customers == 1
    assert usa_slice.churned_customers == 1
    assert usa_slice.total_revenue == ExpectedSeedData.ALICE_EXPECTED_SPEND
    assert usa_slice.arpu == ExpectedSeedData.ALICE_EXPECTED_SPEND

    print(f'\n=== test_dashboard_slice_country_filter ===')
    print(f'\tTotal Customers: {usa_slice.total_customers}')
    print(f'\tActive Customers: {usa_slice.active_customers}')
    print(f'\tChurned Customers: {usa_slice.churned_customers}')
    print(f'\tTotal Revenue: {usa_slice.total_revenue}')
    print(f'\tARPU: {usa_slice.arpu}')


def test_dashboard_slice_segment_filter(db_connection):
    repo = CustomerRepository(db_connection)
    service = AnalyticsService(repo)

    # Filter strictly to VIP tier (Only Alice >= $300.00)
    vip_slice = service.generate_dashboard_slice(segments=[ExpectedSeedData.ALICE_EXPECTED_SEGMENT])

    assert vip_slice.total_customers == 1
    assert vip_slice.filtered_metrics[0].name == ExpectedSeedData.ALICE_NAME

    print(f'\n=== test_dashboard_slice_segment_filter ===')
    print(f'\tTotal Customers: {vip_slice.total_customers}')
    print(f'\tFiltered Metrics: {vip_slice.filtered_metrics}')