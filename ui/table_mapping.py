import streamlit as st
import pandas as pd
from ui.state import handle_df1_click, handle_df2_click, reset_mappings
from logic.shacl_generator import generate_shacl_file

def render_mapping_ui():
    # Get current db connection and selected table from session state
    db = st.session_state.get("db")
    selected_table = st.session_state.get("selected_db_table")

    # Load columns from selected table if connected and table chosen
    if db and selected_table:
        # Assuming your db object has a method get_table_columns(table_name) that returns a list
        st.session_state.database_list = list(db.get_table_columns(selected_table))
    else:
        st.session_state.database_list = []

    # Prepare dataframes for UI display
    db_list = st.session_state.get("database_list", [])
    ontology_list = st.session_state.get("ontology_list", [])
    df1 = pd.DataFrame({'term': db_list})
    df2 = pd.DataFrame({'field': ontology_list})

    st.info(
        f"**Status:** " +
        (f"Selected from Database: **{st.session_state.selected_term_1}**. Now select a match from Ontology."
         if st.session_state.selected_term_1
         else "Select a term from Database to begin mapping.")
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header(f"Columns from: {selected_table or 'No Table Selected'}")
        if not df1.empty:
            st.dataframe(df1, use_container_width=True, hide_index=True)
            st.markdown("---")
            for _, row in df1.iterrows():
                term = row['term']
                is_mapped = term in st.session_state.mappings
                btn_type = "primary" if st.session_state.selected_term_1 == term else "secondary"

                st.button(
                    f"Map: **{term}**",
                    key=f"df1_{term}",
                    on_click=handle_df1_click,
                    args=(term,),
                    disabled=is_mapped,
                    use_container_width=True,
                    type=btn_type
                )
        else:
            st.info("Please select a database table above to load its columns.")

    with col2:
        st.header("Ontology Terms")
        if not df2.empty:
            st.dataframe(df2, use_container_width=True, hide_index=True)
            st.markdown("---")
            if st.session_state.selected_term_1:
                unmapped_terms = [field for field in df2['field'] if field not in st.session_state.mappings.values()]
                selected_ontology_term = st.selectbox(
                    f"Map to: (Ontology term for '{st.session_state.selected_term_1}')",
                    options=[''] + unmapped_terms,
                    index=0,
                    key=f"ontology_dropdown_{st.session_state.selected_term_1}"
                )
                if selected_ontology_term:
                    handle_df2_click(selected_ontology_term)
            else:
                st.info("Select a database column on the left to map to an ontology term.")
        else:
            st.info("Please upload or load an ontology file.")

    # --- Mappings + SHACL output
    st.header("Resulting Mappings", divider='rainbow')

    if st.session_state.mappings:
        for source, dest in st.session_state.mappings.items():
            st.success(f"**{source}** `->` **{dest}`")

        st.subheader("SHACL Input (JSON representation):")
        st.json(st.session_state.mappings)

        shacl_content = generate_shacl_file(
            st.session_state.mappings,
            db_table_name=selected_table
        )

        st.subheader("Generated SHACL File Content (Turtle):")
        st.code(shacl_content, language='turtle')

        st.download_button(
            label="Download SHACL Mappings (.ttl)",
            data=shacl_content,
            file_name=f"shacl_mappings_{selected_table or 'default'}.ttl",
            mime="text/turtle",
            use_container_width=True,
            type="primary"
        )
        st.button("Reset Mappings", on_click=reset_mappings, use_container_width=True, type="secondary")
    else:
        st.write("No mappings created yet.")

