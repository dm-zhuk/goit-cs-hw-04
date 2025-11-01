FROM python:3.10-alpine3.20

WORKDIR /app

RUN pip install --no-cache-dir psycopg2-binary faker

COPY task_manager/create_db.py .

CMD ["python3", "task_manager/create_db.py"]