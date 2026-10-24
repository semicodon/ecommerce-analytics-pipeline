from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "ecommerce.db"
MIGRATIONS_DIR = BASE_DIR / "db" / "migrations"
SEEDS_DIR = BASE_DIR / "db" / "seeds"
REPORTS_DIR = BASE_DIR / "reports"
SEED_FILE = BASE_DIR / "tests" / "conf_test_seeds.py"