import streamlit as st

# --- App Config and State ---
from config import setup_page
from ui.state import init_session_state

# --- UI Components ---
from ui.sidebar import render_sidebar
from ui.table_mapping import render_mapping_ui

# --- Database Connection ---
from database.connectors import db_connection_ui, get_all_db_tables

# --- Setup Page & Session ---
setup_page()
init_session_state()

st.title("🔗 Interactive DataFrame Mapper")
st.markdown("Click a term on the left, then a term on the right to create a one-to-one mapping.")

render_sidebar()

# --- Database Connection UI ---
db = db_connection_ui()

if db:
    all_tables = get_all_db_tables(_db=db)
    if not all_tables.empty:
        st.session_state.db = db
        st.session_state.all_db_tables_info = all_tables
        render_mapping_ui()
    else:
        st.warning("No tables available in database.")
else:
    st.info("Please connect to a database from the sidebar to get started.")
