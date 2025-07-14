import streamlit as st
import os # used for connecting the ontology file to fairmapper
from rdfpandas.graph import to_dataframe
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import SH, RDF, RDFS, XSD

def load_ontology_terms(filename="MDS-Onto-BuiltEnv-PV-Module-v0.3.0.0.ttl"):
    """Loads ontology terms from an uploaded RDF file."""

    try:
        # Get the absolute path to the ontology file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "..", "assets", filename)


        g = Graph()
        g.parse(file_path, format='turtle')
        ontology_df = to_dataframe(g)
        all_terms = list(ontology_df.index)

        # Get namespaces from URIs
        namespaces = sorted(set(
            uri.rsplit("#", 1)[0] if "#" in uri else uri.rsplit("/", 1)[0]
            for uri in all_terms
        ))

        return all_terms, namespaces
    except Exception as e:
        st.error(f"Error loading ontology file '{file_path}': {e}")
        return [], []