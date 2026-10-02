# app/dialect.py
from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.dialects import registry
from sqlalchemy.schema import CreateSequence, DropSequence, Sequence


# --- 1) DBAPI adapter -----------------------------------------------------
class DuckDBAPI:
    """Peers at the `duckdb` module for the attributes SQLAlchemy probes."""
    paramstyle = "qmark"  # DuckDB uses `?` placeholders

    def __init__(self):
        import duckdb
        self.__duckdb = duckdb

    def __getattr__(self, name):
        return getattr(self.__duckdb, name)

    @staticmethod
    def connect(database, read_only=False):
        import duckdb
        return duckdb.connect(database, read_only=read_only)

    @staticmethod
    def is_disconnect():
        return True  # any error on a closed cursor counts as disconnect


# Error needs to be accessible as class attribute
import duckdb
DuckDBAPI.Error = duckdb.Error


# --- 2) Dialect ------------------------------------------------------------
class DuckDBDialect(DefaultDialect):
    name = "duckdb"
    driver = "duckdb"
    supports_native_uuid = True
    paramstyle = "qmark"            # DuckDB uses `?` placeholders
    supports_sane_rowcount = True
    supports_statement_cache = False

    @classmethod
    def import_dbapi(cls):
        return DuckDBAPI

    def do_ping(self, dbapi_connection):
        return False               # skip ping; connections are local

    def do_rollback(self, dbapi_connection):
        # DuckDB doesn't support rollback when no transaction is active
        try:
            dbapi_connection.rollback()
        except Exception:
            pass  # Ignore rollback errors

    def has_table(self, connection, table_name, schema=None):
        # Query DuckDB's information_schema to check if table exists
        query = text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name = :table_name
        """)
        with connection.execute(query, {"table_name": table_name}) as result:
            return result.fetchone() is not None

    def create_connect_args(self, url):
        # "duckdb://app.duckdb" -> database is the file path ("" = memory)
        return (url.database or ":memory:",), {}

    def _get_server_version_info(self, connection):
        # Return a version tuple for DuckDB
        return (1, 0, 0)


# --- 3) Register the scheme -------------------------------------------------
registry.register("duckdb", "app.dialect", "DuckDBDialect")
