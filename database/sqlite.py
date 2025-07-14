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