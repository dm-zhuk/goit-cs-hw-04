import os
import sys
import time
import psycopg2
from psycopg2 import OperationalError


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "456123")
DB_NAME = os.getenv("DB_NAME", "task_manager")


def wait_for_postgres(max_attempts=20, delay=2):
    for attempt in range(1, max_attempts + 1):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                dbname="postgres",
                connect_timeout=3,
            )
            conn.close()
            print("PostgreSQL is ready.")
            return
        except OperationalError as e:
            print(f"Attempt {attempt}/{max_attempts}: {e}")
            time.sleep(delay)
    print("ERROR: PostgreSQL never became ready.")
    sys.exit(1)


def create_database():
    conn = psycopg2.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname="postgres"
    )
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s;", (DB_NAME,))
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"Database '{DB_NAME}' created.")
    else:
        print(f"Database '{DB_NAME}' already exists.")
    cur.close()
    conn.close()


def create_tables():
    conn = psycopg2.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, dbname=DB_NAME
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER NOT NULL REFERENCES status(id),
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    for s in ("new", "in progress", "completed"):
        cur.execute(
            """
            INSERT INTO status (name) VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
        """,
            (s,),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Tables & statuses ready.")


if __name__ == "__main__":
    wait_for_postgres()
    create_database()
    create_tables()


# psql -h localhost -U postgres -d task_manager
