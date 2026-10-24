from dataclasses import dataclass
from typing import List
from src.domains.customers.entity import CustomerSpendSummary
from src.domains.customers.repository import CustomerRepository

@dataclass(frozen=True)
class BusinessKpiReport:
    total_customers: int
    active_customers: int
    churned_customers: int
    total_revenue: float
    arpu: float
    customer_summaries: List[CustomerSpendSummary]


class AnalyticsService:
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo

    def generate_kpi_report(self) -> BusinessKpiReport:
        """Computes high-level executive KPIs from customer domain entities."""
        summaries = self.customer_repo.fetch_customer_spend_summaries()
        total_revenue = sum(c.total_spend for c in summaries)
        active = [c for c in summaries if c.is_active]
        arpu = (total_revenue / len(active)) if active else 0.0

        return BusinessKpiReport(
            total_customers=len(summaries),
            active_customers=len(active),
            churned_customers=len(summaries) - len(active),
            total_revenue=round(total_revenue, 2),
            arpu=round(arpu, 2),
            customer_summaries=summaries,
        )