import os

import psycopg2

# Connection settings come from environment variables (no passwords in code)
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "task_management"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
}

SCHEMA_SQL = """
-- Drop tables if they exist (for clean recreation)
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS status CASCADE;

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status(id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Initial statuses
INSERT INTO status (name) VALUES ('new'), ('in progress'), ('completed');
"""


def main():
    try:
        # "with conn" commits on success and rolls back on error
        with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cursor:
            cursor.execute(SCHEMA_SQL)
        conn.close()
        print("Tables users, status, tasks created")
    except psycopg2.Error as e:
        print(f"Database error: {e}")


if __name__ == "__main__":
    main()
