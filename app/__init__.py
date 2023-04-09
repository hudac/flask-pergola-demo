"""Setup at app startup"""
import os
import time
import sqlalchemy
from flask import Flask
from app import migrate


def init_connection_engine():
    if 'SQLALCHEMY_HOST' not in os.environ:
        return None

    pool = sqlalchemy.create_engine(
        url = sqlalchemy.engine.URL.create(
            drivername=os.environ.get('SQLALCHEMY_DRIVER', default="postgresql+psycopg2"),
            host=os.environ.get('SQLALCHEMY_HOST'),
            port=os.environ.get('SQLALCHEMY_PORT', default="5432"),
            database=os.environ.get('SQLALCHEMY_DB'),
            username=os.environ.get('SQLALCHEMY_USER'),
            password=os.environ.get('SQLALCHEMY_PASSWORD'),
        ), isolation_level="AUTOCOMMIT"  # turns on autocommit for all connections; not ideal, but ok for this demo
    )

    initialized = False
    while not initialized:
        print("connecting to DB...")
        try:
            with pool.connect() as conn:
                print("DB connected.")
                initialized = True
        except:
            time.sleep(3)

    return pool


db = init_connection_engine()
if db is not None:
    migrate.run_sql_migrations(db, "alembic")

app = Flask(__name__)

# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes
