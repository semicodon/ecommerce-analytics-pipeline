import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

from src.core.database import DatabaseManager
from src.domains.customers.repository import CustomerRepository
from src.domains.analytics.service import AnalyticsService
from tests.conftest import SEED_FILE

def load_dashboard_data(
        selected_countries: list[str],
        selected_segments: list[Literal['Inactive','VIP','Standard']],
        seed_data:Path=SEED_FILE
):
    db = DatabaseManager()
    db.run_migrations()
    db.run_seeds(seed_data)

    with db.get_connection() as conn:
        repo = CustomerRepository(conn)
        service = AnalyticsService(repo)
        all_metrics = repo.fetch_customer_window_metrics()
        slice_report = service.generate_dashboard_slice(
            countries=selected_countries,
            segments=selected_segments
        )
        never_ordered = repo.fetch_customers_with_no_orders()

    return all_metrics, slice_report, never_ordered

def render_dashboard() -> None:
    st.set_page_config(
        page_title='E-Commerce Customer Analytics BI',
        page_icon='📈',
        layout='wide'
    )
    st.title("📊 E-Commerce Customer Retention & KPI Dashboard")
    st.caption(
        'Powered by SQLite Views (`v_customer_analytics`), Window Functions (`DENSE_RANK`), '
        'and Domain-Driven Python Services.'
    )

    all_metrics, _, _, = load_dashboard_data(
        selected_countries=[],
        selected_segments=[]
    )

    available_countries = sorted({
        m.country for m in all_metrics
    })
    available_segments = sorted({
        m.segment for m in all_metrics
    })

    # ==============================
    # Sidebar Interactive Filters
    # ==============================
    st.sidebar.header('🔍 Filter Data Mart')
    selected_countries = st.sidebar.multiselect(
        'Country',
        options=available_countries,
        default=available_countries
    )
    selected_segments = st.sidebar.multiselect(
        'Customer Segment',
        options=available_segments,
        default=available_segments
    )

    # Fetch filtered slice based on user selection
    _, slice_report, never_ordered = load_dashboard_data(
        selected_countries=selected_countries,
        selected_segments=selected_segments
    )

    # Top-Level Executive KPI Metric Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Customers", slice_report.total_customers)
    col2.metric("Active Customers", slice_report.active_customers)
    col3.metric("Churned / Inactive", slice_report.churned_customers)
    col4.metric("Total Revenue", f"${slice_report.total_revenue:,.2f}")
    col5.metric("Active ARPU", f"${slice_report.arpu:,.2f}")

    st.divider()

    if not slice_report.filtered_metrics:
        st.warning("No customer records match the selected sidebar filters.")
        return

    # Convert domain entities to DataFrame for visualization & export
    df = pd.DataFrame([
        {
            "Rank": f"#{m.spend_rank}",
            "Customer ID": m.customer_id,
            "Customer Name": m.name,
            "Country": m.country,
            "Segment": m.segment,
            "Completed Orders": m.completed_orders_count,
            "Total Spend ($)": m.total_spend,
            "Global Revenue Share (%)": m.global_revenue_share_pct,
            "Country Revenue Share (%)": m.country_revenue_share_pct,
            "Last Order Date": m.last_order_date or "Never Ordered",
        }
        for m in slice_report.filtered_metrics
    ])

    # ==============================
    # Chart Selection
    # ==============================
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Total Completed Spend by Customer ($ USD)")
        spend_chart_df = df.set_index("Customer Name")[["Total Spend ($)"]]
        st.bar_chart(spend_chart_df, color="#1e3a8a")

    with chart_col2:
        st.subheader("Revenue Contribution by Country ($ USD)")
        country_df = (
            df.groupby("Country", as_index=True)[["Total Spend ($)"]]
            .sum()
            .sort_values(by="Total Spend ($)", ascending=False)
        )
        st.bar_chart(country_df, color="#0f766e")

    st.divider()

    # ==============================
    # SQL Window Function Leaderboard & CSV Export
    # ==============================
    header_col, download_col = st.columns([3, 1])

    with header_col:
        st.subheader("📋 Customer RFM & Window Ranking Mart")

    with download_col:
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Filtered CSV Mart",
            data=csv_bytes,
            file_name="filtered_customer_kpi_mart.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.dataframe(df, use_container_width=True, hide_index=True)

    # ==============================
    # Churn Risk Callout
    # ==============================
    if never_ordered:
        st.info(
            f"**Churn Alert — Customers With Zero Historical Orders:** {', '.join(never_ordered)}"
        )


if __name__ == "__main__":
    render_dashboard()