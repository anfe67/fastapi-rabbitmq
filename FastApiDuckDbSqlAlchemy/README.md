# FastAPI + DuckDB + SQLAlchemy

A simple example demonstrating how to use DuckDB with SQLAlchemy 2.x and FastAPI.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **DuckDB** - In-process SQL database with analytical capabilities
- **SQLAlchemy 2.x** - Python SQL toolkit and ORM
- **Uvicorn** - ASGI server

## Features

- Custom SQLAlchemy dialect for DuckDB
- RESTful API for managing books
- File-backed database (persistent storage)
- Manual ID generation (DuckDB doesn't support autoincrement like traditional databases)

## Installation

```bash
uv sync
```

## Running the Application

```bash
uv run uvicorn app.main:create_app --factory
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints

### Books

- `GET /books` - List all books (with optional filtering by genre)
- `GET /books/{book_id}` - Get a specific book by ID
- `POST /books` - Create a new book
- `DELETE /books/{book_id}` - Delete a book

### Summary

- `GET /books/summary` - Get genre statistics (count, earliest/latest year, revenue)

### Example Usage

```bash
# Create a book
curl -X POST localhost:8000/books \
  -d '{"title":"Neuromancer","year":1984,"genre":"sci-fi"}' \
  -H 'Content-Type: application/json'

# List all books
curl localhost:8000/books

# Get a specific book
curl localhost:8000/books/1

# Get genre summary
curl localhost:8000/books/summary
```

## Database

The database is stored in `app.duckdb` in the project root. This is a file-backed DuckDB database, so data persists between application restarts.

To use an in-memory database instead, change the connection string in `app/db.py` from `"duckdb://app.duckdb"` to `"duckdb://:memory:"`.

## Custom DuckDB Dialect

This project includes a custom SQLAlchemy dialect (`app/dialect.py`) that bridges SQLAlchemy with DuckDB. Key implementation details:

- **DBAPI Adapter**: Wraps DuckDB's native Python module to provide SQLAlchemy-compatible interface
- **No Autoincrement**: DuckDB doesn't support traditional autoincrement, so IDs are generated manually using `MAX(id) + 1`
- **Statement Caching**: Disabled for simplicity (`supports_statement_cache = False`)
- **Rollback Handling**: DuckDB doesn't allow rollback when no transaction is active, so errors are silently ignored

## Project Structure

```
app/
├── __init__.py
├── db.py          # Database engine, session, and initialization
├── dialect.py     # Custom DuckDB SQLAlchemy dialect
├── main.py        # FastAPI application factory
├── models.py      # SQLAlchemy ORM models
└── routers/
    └── books.py   # Book API endpoints
```
