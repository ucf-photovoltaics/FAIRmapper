import streamlit as st

# --- Session State Initialization ---
def init_session_state():

    if 'mappings' not in st.session_state:
        st.session_state.mappings = {}
    if 'selected_term_1' not in st.session_state:
        st.session_state.selected_term_1 = None
    if 'selected_db_table' not in st.session_state:
        st.session_state.selected_db_table = None
    if 'all_db_tables_info' not in st.session_state:
        st.session_state.all_db_tables_info = None


# --- Helper Functions ---
def handle_df1_click(term):
    """Callback function to handle selection from the first dataframe."""
    st.session_state.selected_term_1 = term

def handle_df2_click(field):
    """Callback function to handle selection from the second dataframe and create a mapping."""
    if st.session_state.selected_term_1:
        st.session_state.mappings[st.session_state.selected_term_1] = field
        # Reset selection after mapping
        st.session_state.selected_term_1 = None

def reset_mappings():
    """Clears all existing mappings and selections."""
    st.session_state.mappings = {}
    st.session_state.selected_term_1 = None