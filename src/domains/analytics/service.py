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

@dataclass(frozen=True)
class DashboardSliceReport:
    total_customers: int
    active_customers: int
    churned_customers: int
    total_revenue: float
    arpu: float
    filtered_metrics: List[CustomerWindowMetrics]

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

    def generate_dashboard_slice(self,
                                 countries: Optional[List[str]]=None,
                                 segments: Optional[List[str]]=None,
                                 ) -> DashboardSliceReport:
        """Filters window metrics by country/segment and recalculates slice KPIs."""
        all_metrics = self.customer_repo.fetch_customer_window_metrics()

        filtered = [
            m for m in all_metrics
            if (not countries or m.country in countries)
            and (not segments or m.segment in segments)
        ]

        total_revenue = sum(m.total_spend for m in filtered)
        active = [m for m in filtered if m.is_active]
        arpu = (total_revenue / len(active)) if active else 0.0

        return DashboardSliceReport(
            total_customers=len(filtered),
            active_customers=len(active),
            churned_customers=len(filtered) - len(active),
            total_revenue=round(total_revenue, 2),
            arpu=round(arpu, 2),
            filtered_metrics=filtered,
        )