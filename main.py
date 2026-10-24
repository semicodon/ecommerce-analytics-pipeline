from src.core.database import DatabaseManager
from src.domains.customers.repository import CustomerRepository
from src.domains.analytics.service import AnalyticsService
from src.domains.analytics.reports import ReportGenerator


def run_pipeline() -> None:
    db = DatabaseManager()
    db.run_migrations()
    db.run_seeds()

    with db.get_connection() as conn:
        customer_repo = CustomerRepository(conn)
        analytics_service = AnalyticsService(customer_repo)

        report = analytics_service.generate_kpi_report()

        print("\n================ E-COMMERCE KPI REPORT ================")
        print(f"Total Customers   : {report.total_customers}")
        print(f"Active Customers  : {report.active_customers}")
        print(f"Churned/Inactive  : {report.churned_customers}")
        print(f"Total Revenue     : ${report.total_revenue:,.2f}")
        print(f"ARPU (Active)     : ${report.arpu:,.2f}")
        print("-------------------------------------------------------")
        for c in report.customer_summaries:
            print(f"{c.name:<16} | {c.country:<7} | ${c.total_spend:>7.2f} | {c.segment}")
        print("=======================================================\n")

        chart_path = ReportGenerator.export_spend_chart(report.customer_summaries)
        print(f"[OK] Visual report saved to: {chart_path}")


if __name__ == "__main__":
    run_pipeline()