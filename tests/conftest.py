import pytest
from pathlib import Path
from src.core.database import DatabaseManager


@pytest.fixture
def db_connection(tmp_path: Path):
    """Provide an isolated, migrated, and seeded database connection per test."""
    test_db_file = tmp_path / "test_ecommerce.db"
    db = DatabaseManager(db_path=test_db_file)
    conn = None

    try:
        db.run_migrations()
        db.run_seeds()

        conn = db.get_connection()
        if conn is None:
            pytest.fail("Database connection could not be established.")

        yield conn

    finally:
        if conn is not None:
            conn.close()