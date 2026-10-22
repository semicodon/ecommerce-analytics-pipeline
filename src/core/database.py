import sqlite3
from pathlib import Path
from src.core.config import DB_PATH, MIGRATIONS_DIR, SEEDS_DIR


class DatabaseManager:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Creates a database connection with Row factory and Foreign Keys enforced."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def run_migrations(self) -> None:
        """Applies all SQL files in db/migrations/ in alphabetical order."""
        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
        if not migration_files:
            raise FileNotFoundError(f"No migration files found in {MIGRATIONS_DIR}")

        with self.get_connection() as conn:
            for sql_file in migration_files:
                conn.executescript(sql_file.read_text(encoding="utf-8"))

    def run_seeds(self) -> None:
        """Executes all seed SQL files in db/seeds/ in alphabetical order."""
        seed_files = sorted(SEEDS_DIR.glob("*.sql"))
        if not seed_files:
            raise FileNotFoundError(f"No seed files found in {SEEDS_DIR}")

        with self.get_connection() as conn:
            for seed_file in seed_files:
                conn.executescript(seed_file.read_text(encoding="utf-8"))