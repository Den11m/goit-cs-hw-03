import random

import psycopg2
from faker import Faker

from create_tables import DB_CONFIG

NUM_USERS = 10
NUM_TASKS = 30

fake = Faker()


def seed(cursor):
    """Insert random users and tasks that use existing statuses"""
    users = [(fake.name(), fake.unique.email()) for _ in range(NUM_USERS)]
    cursor.executemany("INSERT INTO users (fullname, email) VALUES (%s, %s)", users)

    cursor.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT id FROM users")
    # Last 2 users get no tasks, so query 4 returns something
    user_ids = [row[0] for row in cursor.fetchall()][:-2]

    tasks = [
        (
            fake.sentence(nb_words=4)[:-1],
            # ~20% of tasks without description, so query 12 returns something
            fake.text(max_nb_chars=200) if random.random() > 0.2 else None,
            random.choice(status_ids),
            random.choice(user_ids),
        )
        for _ in range(NUM_TASKS)
    ]
    cursor.executemany(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
        tasks,
    )


def main():
    try:
        # "with conn" commits on success and rolls back on error
        with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cursor:
            seed(cursor)
        conn.close()
        print(f"Inserted {NUM_USERS} users and {NUM_TASKS} tasks")
    except psycopg2.Error as e:
        print(f"Database error: {e}")


if __name__ == "__main__":
    main()
