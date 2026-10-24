from src.domains.analytics.reports import ReportGenerator
from src.domains.analytics.service import AnalyticsService
from src.domains.customers.repository import CustomerRepository
from conf_test_seeds import ExpectedSeedData

def test_analytics_service_kpi_report(db_connection):
    repo = CustomerRepository(db_connection)
    service = AnalyticsService(repo)
    report = service.generate_kpi_report()

    assert report.total_customers == ExpectedSeedData.EXPECTED_TOTAL_CUSTOMERS
    assert report.active_customers == ExpectedSeedData.EXPECTED_ACTIVE_CUSTOMERS
    assert report.churned_customers == ExpectedSeedData.EXPECTED_CHURNED_CUSTOMERS
    assert report.total_revenue == ExpectedSeedData.EXPECTED_TOTAL_REVENUE
    assert report.arpu == ExpectedSeedData.EXPECTED_ARPU

    print(f'\n==== test_analytics_service_kpi_report ====')
    print(f'\tTotal Customers: {report.total_customers}')
    print(f'\tActive Customers: {report.active_customers}')
    print(f'\tChurned Customers: {report.churned_customers}')
    print(f'\tTotal Revenue: {report.total_revenue}')
    print(f'\tArpu: {report.arpu}')

def test_report_chart_generation(db_connection, tmp_path: Path):
    repo = CustomerRepository(db_connection)
    summaries = repo.fetch_customer_spend_summaries()

    chart_file = ReportGenerator.export_spend_chart(summaries, output_dir=tmp_path)

    assert chart_file.exists()
    assert chart_file.stat().st_size > 0