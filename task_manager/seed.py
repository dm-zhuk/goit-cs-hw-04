import psycopg2
from faker import Faker
import random


fake = Faker()

# Параметри підключення до бази даних
db_params = {
    "dbname": "task_manager",
    "user": "postgres",
    "password": "456123",
    "host": "localhost",
    "port": "5432",
}

conn = psycopg2.connect(**db_params)
cur = conn.cursor()


cur.execute("SELECT id FROM status;")
status_ids = [row[0] for row in cur.fetchall()]

# Вставка користувачів
for _ in range(5):
    fullname = fake.name()
    email = fake.unique.email()
    cur.execute(
        "INSERT INTO users (fullname, email) VALUES (%s, %s);",
        (fullname, email),
    )


cur.execute("SELECT id FROM users;")
user_ids = [row[0] for row in cur.fetchall()]

# Вставка завдань
try:
    for _ in range(10):
        title = fake.sentence(nb_words=4).strip(".")
        description = fake.paragraph()
        status_id = random.choice(status_ids)
        user_id = random.choice(user_ids)
        cur.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);",
            (title, description, status_id, user_id),
        )

    conn.commit()
except psycopg2.Error as e:
    print(f"Помилка при заповненні бази даних: {e}")
    conn.rollback()
finally:
    if conn:
        cur.close()
        conn.close()

print("Database seeded successfully!")
