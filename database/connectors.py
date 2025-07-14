import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

class DatabaseConnector:
    def __init__(self, db_type, **kwargs):
        self.db_type = db_type
        self.kwargs = kwargs
        self.engine = None

    def connect(self):
        try:
            if self.db_type == "postgres":
                user = self.kwargs.get("user")
                password = self.kwargs.get("password")
                host = self.kwargs.get("host")
                port = self.kwargs.get("port")
                database = self.kwargs.get("database")
                url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
                self.engine = create_engine(url)
            elif self.db_type == "mysql":
                # add mysql connection string similarly here
                pass
            elif self.db_type == "sqlite":
                db_path = self.kwargs.get("db_path")
                url = f"sqlite:///{db_path}"
                self.engine = create_engine(url)
            else:
                st.error(f"Unsupported database type: {self.db_type}")
                return False

            # Test connection by connecting once
            with self.engine.connect() as conn:
                pass
            return True
        except Exception as e:
            st.error(f"Failed to connect: {e}")
            return False

    def get_all_tables(self):
        try:
            if self.db_type == "postgres":
                query = """
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
                """
            elif self.db_type == "mysql":
                query = "SHOW TABLES"
            elif self.db_type == "sqlite":
                query = "SELECT name FROM sqlite_master WHERE type='table';"
            else:
                return []

            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                tables = [row[0] for row in result]
                return tables
        except Exception as e:
            st.error(f"Failed to fetch tables: {e}")
            return []

    def get_table_columns(self, table_name):
        try:
            query = f"SELECT * FROM {table_name} LIMIT 0"
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return result.keys()  # column names
        except Exception as e:
            import streamlit as st
            st.error(f"Failed to load columns for {table_name}: {e}")
            return []
        


def db_connection_ui():
    st.sidebar.header("🔌 Database Configuration")
    db_type = st.sidebar.selectbox("Choose database type", ["postgres", "mysql", "sqlite"])

    credentials = {}
    if db_type == "sqlite":
        credentials['db_path'] = st.sidebar.text_input("SQLite DB Path", value="path/to/your.db")
    else:
        credentials['user'] = st.sidebar.text_input("Username")
        credentials['password'] = st.sidebar.text_input("Password", type="password")
        credentials['host'] = st.sidebar.text_input("Host", value="localhost")
        credentials['port'] = st.sidebar.number_input("Port", value=5432 if db_type == "postgres" else 3306)
        credentials['database'] = st.sidebar.text_input("Database Name")

    if st.sidebar.button("Connect to Database"):
        db = DatabaseConnector(db_type, **credentials)
        if db.connect():
            st.sidebar.success(f"Connected to {db_type} database!")
            return db
        else:
            st.sidebar.error("Failed to connect.")
    return None

@st.cache_data
def get_all_db_tables(_db):
    if _db:
        tables = _db.get_all_tables()
        import pandas as pd
        return pd.DataFrame(tables, columns=['table_name'])
    else:
        import pandas as pd
        return pd.DataFrame(columns=['table_name'])

