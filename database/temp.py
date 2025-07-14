# database/__init__.py
# (can be empty or include shared exports)

# database/connectors.py
import streamlit as st
import pandas as pd

from database.postgres import PostgresDB
from database.mysql import MySQLDB
from database.sqlite import SQLiteDB

# This function acts as a factory for different DB types
def get_database_connection(db_type, **kwargs):
    try:
        if db_type == 'postgres':
            return PostgresDB(**kwargs)
        elif db_type == 'mysql':
            return MySQLDB(**kwargs)
        elif db_type == 'sqlite':
            return SQLiteDB(**kwargs)
        else:
            st.error(f"Unsupported database type: {db_type}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to {db_type} database: {e}")
        return None

# This will be used inside the Streamlit app
@st.cache_data
def get_all_db_tables(db=None):
    if db:
        return db.get_table_names_and_comments()
    return pd.DataFrame(columns=['table_name', 'table_comment'])


def load_db_columns(db, table_name):
    if db and table_name:
        query = f"SELECT * FROM instrument_data.{table_name} LIMIT 0"
        df_schema = db.read_records(query)
        return list(df_schema.columns)
    return []


# database/postgres.py
import psycopg2
import pandas as pd

class PostgresDB:
    def __init__(self, user, database, host='localhost', password='', port=5432):
        self.conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

    def get_table_names_and_comments(self):
        query = """
        SELECT table_name, obj_description(('instrument_data.' || table_name)::regclass) AS table_comment
        FROM information_schema.tables
        WHERE table_schema = 'instrument_data';
        """
        return pd.read_sql(query, self.conn)

    def read_records(self, query):
        return pd.read_sql(query, self.conn)


# database/mysql.py
import mysql.connector
import pandas as pd

class MySQLDB:
    def __init__(self, user, database, host='localhost', password='', port=3306):
        self.conn = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )

    def get_table_names_and_comments(self):
        cursor = self.conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        return pd.DataFrame(tables, columns=['table_name'])

    def read_records(self, query):
        return pd.read_sql(query, self.conn)


# database/sqlite.py
import sqlite3
import pandas as pd

class SQLiteDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def get_table_names_and_comments(self):
        query = "SELECT name as table_name FROM sqlite_master WHERE type='table';"
        return pd.read_sql(query, self.conn)

    def read_records(self, query):
        return pd.read_sql(query, self.conn)
