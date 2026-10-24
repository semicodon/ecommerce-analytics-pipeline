# E-Commerce Customer Retention & Analytics Pipeline

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57)
![Pytest](https://img.shields.io/badge/Tests-Pytest-0A9EDC)
![CI Status](https://img.shields.io/badge/CI-GitHub_Actions-2088FF)

A production-structured data analytics and reporting pipeline that models enterprise analytics engineering workflows. This project demonstrates the separation of **SQL push-down aggregations**, **domain-driven Python business logic**, **idempotent database migrations/seeding**, and **isolated automated testing**.

---

## 1. Business Problem & Objectives

Analytics and BI teams frequently need to combine relational transaction history with business-tier segmentation to answer three core questions:
1. **Customer Spend & Activity:** Which customers drive top-line revenue across completed orders, and how does SQL handle customers with only cancelled or zero orders?
2. **Churn & Inactivity Detection:** Which signed-up customers have never placed an order or have become inactive?
3. **Executive KPI Reporting:** What are the current Total Revenue, Active Customer count, Churned Customer count, and Average Revenue Per Active User ($\text{ARPU}$)?

---

## 2. Engineering Architecture

Rather than placing raw SQL and plotting logic inside a single monolithic script, this repository implements a layered workplace architecture:

* **Migration & Seed Separation (`db/`):** Schema definitions (`DDL` in `db/migrations/`) are strictly decoupled from sample data population (`DML` in `db/seeds/`). Migrations enforce referential integrity (`PRAGMA foreign_keys = ON`) and domain constraints (`CHECK`), while seeds are written idempotently (`INSERT OR IGNORE`).
* **Core Infrastructure (`src/core/`):** Centralizes filesystem paths (`config.py`) and manages database connections, ordered migration execution, and row factories (`database.py`).
* **Domain & Repository Pattern (`src/domains/`):**
    * **Entities (`entity.py`):** Immutable Python `@dataclass(frozen=True)` models holding pure business rules (e.g., VIP vs. Standard vs. Churned segmentation) with zero database dependencies.
    * **Repositories (`repository.py`):** Encapsulates analytical SQL queries (`LEFT JOIN`, `COALESCE`, `COUNT(DISTINCT ...)`) and maps database rows into typed domain entities.
    * **Services & Reporting (`service.py`, `reports.py`):** Orchestrates KPI calculations and exports high-resolution stakeholder charts using a headless `matplotlib` backend (`Agg`).
* **Isolated Test Suite (`tests/`):** Uses `pytest` fixtures with `tmp_path` so every test spins up an isolated, freshly migrated and seeded SQLite database without polluting local development data.

---

## 3. Repository Structure
## System Architecture

```text
ecommerce-analytics-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml                                    # Automated CI test suite & daily scheduled Cron ETL
├── db/
│   ├── migrations/
│   │   ├── 001_create_customers.sql                  # DDL: Customers table
│   │   ├── 002_create_orders.sql                     # DDL: Orders table with CHECK & FK constraints
│   │   ├── 003_create_order_items.sql                # DDL: Order line items table
│   │   └── 004_create_customer_analytics_view.sql    # SQL View: CTEs + DENSE_RANK & revenue share windows
│   └── seeds/
│       └── dev_seed_inactive.sql                     # DML: Idempotent development seed data - kept here for                  
│                                                     #     architecture reference only
├── reports/                                          # Generated BI charts (.png) & Data Mart exports (.csv)
├── src/
│   ├── core/
│   │   ├── config.py                                 # Centralized filesystem & environment paths
│   │   └── database.py                               # Connection manager, migration & seed runner
│   ├── domains/
│   │   ├── customers/
│   │   │   ├── entity.py                             # Immutable domain models & segmentation rules
│   │   │   └── repository.py                         # SQL data access & view mapping layer
│   │   └── analytics/
│   │       ├── service.py                            # Executive KPI calculation & dashboard slice filtering
│   │       └── reports.py                            # Matplotlib chart & CSV Data Mart exporters
│   └── dashboard.py                                  # Interactive Streamlit BI web application
├── tests/
│   ├── conf_test_seeds.py                            # Centralized test seed records & expected constants
│   ├── conftest.py                                   # Isolated tmp_path DB fixtures & test factories
│   ├── test_analytics_report.py                      # KPI service, dashboard filter & export tests
│   ├── test_customer_spend_summary.py                # Parameterized repository & SQL View tests
│   ├── test_dashboard_analytics.py                   # Streamlit dashboard analytics tests
│   └── test_database.py                              # DB migration & seed tests
├── pytest.ini
├── main.py                                           # CLI production ETL entrypoint
├── requirements.txt
└── README.md                                    

```

---

## 4. Database Schema & SQL Complexity

### Relational Schema
* **`customers`**: `customer_id` (PK), `name`, `country`, `signup_date`
* **`orders`**: `order_id` (PK), `customer_id` (FK $\rightarrow$ `customers.customer_id`), `order_date`, `status` (`PENDING`, `COMPLETED`, `CANCELLED`)
* **`order_items`**: `item_id` (PK), `order_id` (FK $\rightarrow$ `orders.order_id`), `product_name`, `quantity`, `price`

### Push-Down SQL Design
In `CustomerRepository.fetch_customer_spend_summaries()`, filtering for `o.status = 'COMPLETED'` is placed directly inside the `LEFT JOIN ... ON` predicate rather than the `WHERE` clause:

```sql
SELECT 
    c.customer_id,
    c.name,
    c.country,
    COUNT(DISTINCT o.order_id) AS completed_orders_count,
    COALESCE(SUM(oi.quantity * oi.price), 0.0) AS total_spend,
    MAX(o.order_date) AS last_order_date
FROM customers c
LEFT JOIN orders o 
    ON c.customer_id = o.customer_id 
    AND o.status = 'COMPLETED'
LEFT JOIN order_items oi 
    ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.name, c.country
ORDER BY total_spend DESC, c.customer_id ASC;
```

Placing `o.status = 'COMPLETED'` in the `ON` clause preserves customers who have zero orders (or only cancelled orders) with `$0.00` spend via `COALESCE`, preventing them from being filtered out prematurely.
* **Query Complexity:** Scanning and hash-aggregating $N$ order line items into $m$ distinct customers runs in $O(N)$ time, followed by comparison-based sorting in $O(m \log m)$ time, yielding an overall execution complexity of $O(N + m \log m)$.

---

## 5. Quickstart & Local Usage

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/<your-username>/ecommerce-analytics-pipeline.git
cd ecommerce-analytics-pipeline

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Analytics Pipeline
Execute the application entrypoint from the project root:
```bash
python -m main
```

**Expected Terminal Output:**
```text
================ E-COMMERCE KPI REPORT ================
Total Customers   : 5
Active Customers  : 3
Churned/Inactive  : 2
Total Revenue     : $665.00
ARPU (Active)     : $221.67
-------------------------------------------------------
Alice Johnson    | USA     | $ 550.00 | VIP
Diana Prince     | UK      | $  65.00 | Standard
Bob Smith        | Canada  | $  50.00 | Standard
Charlie Brown    | USA     | $   0.00 | Churned / Inactive
Evan Wright      | Canada  | $   0.00 | Churned / Inactive
=======================================================

[OK] Visual report saved to: .../reports/customer_spend.png
```

### 3. Run the Automated Test Suite
```bash
pytest -v -s
```

### 4. Launch the Interactive Streamlit BI Dashboard
Starts a local BI web server at `http://localhost:8501` with country/segment multi-select filters, real-time KPI cards, interactive charts, and one-click CSV Data Mart downloads:
```bash
streamlit run src/dashboard.py
```
![alt text](reports/dashboard_preview.png)

