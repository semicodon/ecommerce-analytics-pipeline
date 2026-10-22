import sqlite3
import pytest


def test_database_connection(db_connection):
    assert db_connection is not None


def test_migrations_created_all_tables(db_connection):
    cursor = db_connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    )
    tables = {row["name"] for row in cursor.fetchall()}
    assert {"customers", "orders", "order_items"}.issubset(tables)


def test_foreign_key_constraints_are_enforced(db_connection):
    """Verify invalid customer_id on orders raises an IntegrityError."""
    with pytest.raises(sqlite3.IntegrityError):
        db_connection.execute(
            "INSERT INTO orders (customer_id, order_date, status) VALUES (9999, '2023-10-01', 'COMPLETED');"
        )