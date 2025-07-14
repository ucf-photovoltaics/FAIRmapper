import streamlit as st
from logic.ontology_loader import load_ontology_terms
from ui.state import reset_mappings
import pandas as pd

def render_sidebar():
    st.header("Configuration", divider='blue')
    col_config_left, col_config_right = st.columns(2, gap="large")

    # Get current db connection object from session state
    db = st.session_state.get("db")

    with col_config_left:
        st.subheader("Database Tables Overview")

        # Fetch all tables info if not already cached
        if db and st.session_state.get("all_db_tables_info") is None:
            tables = db.get_all_tables()  # This returns a list
            # Convert to DataFrame for UI display consistency
            st.session_state.all_db_tables_info = pd.DataFrame(tables, columns=['table_name'])

        all_tables_df = st.session_state.get("all_db_tables_info")

        if all_tables_df is not None and not all_tables_df.empty:
            st.dataframe(all_tables_df, use_container_width=True, hide_index=True)

            table_names = all_tables_df['table_name'].tolist()
            selected_db_table = st.selectbox(
                "Select a Database Table for Mapping (Source Columns)",
                options=[''] + table_names,
                index=0 if st.session_state.get("selected_db_table") is None else (
                    table_names.index(st.session_state.selected_db_table) + 1
                    if st.session_state.selected_db_table in table_names else 0),
                key="db_table_selector"
            )
            if selected_db_table and selected_db_table != st.session_state.get("selected_db_table"):
                st.session_state.selected_db_table = selected_db_table
                reset_mappings()
        else:
            st.warning("No database tables found or connection error. Check your DB connection.")

    with col_config_right:
        st.subheader("Upload Ontology File (optional)")
        # Future upload widget here

    # Fetch columns for selected table and update session state
    if db and st.session_state.get("selected_db_table"):
        st.session_state.database_list = list(db.get_table_columns(st.session_state.selected_db_table))
    else:
        st.session_state.database_list = []

    # Load ontology terms and namespaces into session state
    st.session_state.ontology_list, st.session_state.available_namespaces = load_ontology_terms()

