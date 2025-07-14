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