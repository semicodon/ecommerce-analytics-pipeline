import csv
from pathlib import Path
from typing import List
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.core.config import REPORTS_DIR
from src.domains.customers.entity import CustomerSpendSummary, CustomerWindowMetrics

class ReportGenerator:
    
    @staticmethod
    def export_spend_chart(
            customers: List[CustomerSpendSummary],
            output_dir: Path = REPORTS_DIR,
            filename: str = "customer_spend.png",
    ) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

        names = [c.name for c in customers]
        spends = [c.total_spend for c in customers]

        fig, ax = plt.subplots(figsize=(9, 4.5))
        bars = ax.bar(names, spends, color="#1e3a8a")
        ax.set_title("Total Completed Spend by Customer ($ USD)", fontsize=13, fontweight="bold")
        ax.set_ylabel("Spend ($ USD)")
        ax.grid(axis="y", linestyle="--", alpha=0.6)

        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"${height:,.0f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
            )

        fig.tight_layout()
        fig.savefig(output_path, dpi=300)
        plt.close(fig)
        return output_path

    @staticmethod
    def export_kpi_mart_csv(
            metrics: List[CustomerWindowMetrics],
            output_dir: Path=REPORTS_DIR,
            filename: str='customer_kpi_mart.csv',
    ) -> Path:
        """Exports an enriched BI Data Mart CSV for Power BI / Excel Integration."""
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

        headers = [
            "customer_id",
            "name",
            "country",
            "segment",
            "completed_orders_count",
            "total_spend",
            "spend_rank",
            "global_revenue_share_pct",
            "country_revenue_share_pct",
            "last_order_date",
        ]

        with output_path.open(mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for m in metrics:
                writer.writerow([
                    m.customer_id,
                    m.name,
                    m.country,
                    m.segment,
                    m.completed_orders_count,
                    f"{m.total_spend:.2f}",
                    m.spend_rank,
                    f"{m.global_revenue_share_pct:.2f}",
                    f"{m.country_revenue_share_pct:.2f}",
                    m.last_order_date or "N/A",
                ])
        return output_path