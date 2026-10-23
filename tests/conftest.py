import pytest
from pathlib import Path
from src.core.database import DatabaseManager

SEED_FILE = Path(__file__).parent / "conf_test_seeds.py"

@pytest.fixture
def empty_db(tmp_path: Path):
    """Provides a clean, migrated database with zero rows"""
    db = DatabaseManager(db_path=tmp_path/ "test_ecommerce.db")
    db.run_migrations()
    conn = db.get_connection()
    try:
        yield conn
    finally:
        conn.close()

@pytest.fixture
def db_connection(tmp_path: Path, seed_file: Path=SEED_FILE):
    """Provide an isolated, migrated, and seeded database connection per test."""
    test_db_file = tmp_path / "test_ecommerce.db"
    db = DatabaseManager(db_path=test_db_file)
    conn = None

    try:
        db.run_migrations()
        db.run_seeds(seed_file=seed_file)

        conn = db.get_connection()
        if conn is None:
            pytest.fail("Database connection could not be established.")

        yield conn

    finally:
        if conn is not None:
            conn.close()