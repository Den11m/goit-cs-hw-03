# Task Management System - PostgreSQL

- `create_tables.py` — creates tables `users`, `status`, `tasks` and inserts statuses `new`, `in progress`, `completed`
- `seed.py` — fills the tables with test data using Faker
- `queries.sql` — 14 SQL queries from the assignment
- `requirements.txt` — Python dependencies

## Setup

Run from the `task1_postgres` folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Connection settings are read from environment variables:

| Variable | Default |
|---|---|
| `POSTGRES_PASSWORD` | — (required) |
| `POSTGRES_DB` | `task_management` |
| `POSTGRES_USER` | `postgres` |
| `POSTGRES_HOST` | `localhost` |
| `POSTGRES_PORT` | `5432` |

```bash
export POSTGRES_PASSWORD=your_password
```

Start PostgreSQL in Docker (or use a local PostgreSQL with database `task_management`):

```bash
docker run --name task-pg -d -p 5432:5432 -e POSTGRES_DB=task_management -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD postgres:16
```

## Run

```bash
# 1. Create tables
python create_tables.py

# 2. Seed test data (10 users, 30 tasks)
python seed.py

# 3. Run queries
docker exec -i task-pg psql -U postgres -d task_management < queries.sql
```

With local psql use `psql -U postgres -d task_management -f queries.sql` instead of `docker exec`.

Queries use example values (`user_id = 1`, domain `example.com`, ...) — change them as needed.
