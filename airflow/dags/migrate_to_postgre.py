import datetime

from pymongo import MongoClient
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import logging
from psycopg2 import connect


def migrate_to_postgre() -> None:
    with MongoClient("mongodb://root:123456@www.vcrostin.space:27017") as connection:
        user_sessions = connection["database"]["user_sessions"]
        support_tickets = connection["database"]["support_tickets"]

        """
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                user_id TEXT,
                start_time INT,
                end_time INT,
                pages_visited INT,
                device TEXT,
                actions JSONB
            )
        """

        """
            CREATE TABLE IF NOT EXISTS support_tickets (
                    ticket_id TEXT PRIMARY KEY,
                    user_id TEXT,
                    status TEXT,
                    issue_type TEXT,
                    created_at INT,
                    updated_at INT
                )
        """

        sessions = user_sessions.find({"start_time": {"$gte": 0}})
        tickets = support_tickets.find({"updated_at": {"$gte": 0}})

        with connect(
                dbname='airflow',
                user='airflow',
                password='airflow',
                host='www.vcrostin.space') as cursor:
            for session in sessions:
                cursor.execute(
                    query="""
                    INSERT INTO user_sessions
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (session_id) DO NOTHING
                """,
                    vars=(
                        session["session_id"],
                        session["user_id"],
                        session["start_time"],
                        session["end_time"],
                        session["pages_visited"],
                        session["device"],
                        json.dumps(session["actions"]),
                    ),
                )

            for ticket in tickets:
                cursor.execute(
                    query="""
                    INSERT INTO support_tickets
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticket_id) DO NOTHING
                """,
                    vars=(
                        ticket["ticket_id"],
                        ticket["user_id"],
                        ticket["status"],
                        ticket["issue_type"],
                        ticket["created_at"],
                        ticket["updated_at"],
                    ),
                )

            cursor.commit()


with DAG(
    "migrate_to_postgre",
    default_args={'owner': 'airflow'},
    schedule_interval="@dayly",
    start_date=datetime(2024, 1, 1),
) as dag:
    migrate_task = PythonOperator(
        task_id="migrate_to_postgre", python_callable=migrate_to_postgre
    )