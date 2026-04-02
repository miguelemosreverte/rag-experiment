# SQL Query Executor Tool

## Description
Executes read-only SQL queries against a PostgreSQL database and returns results as structured JSON. Only SELECT statements are permitted; all write operations (INSERT, UPDATE, DELETE, DROP) are blocked at the parser level.

## Connection
Uses connection pool managed by `asyncpg`. Connection string from environment variable `DATABASE_URL`.

## Parameters
- `query` (required): SQL SELECT statement as a string.
- `params` (optional): List of bind parameters for parameterized queries.
- `limit` (optional): Maximum rows to return. Default: 100. Max: 10,000.
- `timeout` (optional): Query timeout in seconds. Default: 30.

## Example Usage
```python
result = sql_query(
    query="SELECT name, email FROM users WHERE created_at > $1 ORDER BY created_at DESC",
    params=["2024-01-01"],
    limit=50
)
# Returns: {"columns": ["name", "email"], "rows": [...], "row_count": 42}
```

## Schema Discovery
Use `sql_query(query="SELECT table_name FROM information_schema.tables WHERE table_schema='public'")` to list available tables.

## Security
- Queries are parsed and validated before execution
- Only SELECT and WITH (CTE) statements allowed
- Connection uses a read-only database role
- All queries are logged with timestamp and execution time

## Performance
- Connection pool: 5-20 connections
- Query results cached for 60 seconds (cache key: SHA256 of query + params)
- Large result sets are streamed in chunks of 1,000 rows
