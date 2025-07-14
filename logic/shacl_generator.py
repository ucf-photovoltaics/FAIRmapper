from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import SH, RDF, RDFS, XSD
from io import StringIO # To read uploaded file content



def generate_shacl_file(mappings, db_table_name="DatabaseTable"):
    """
    Generates a SHACL Turtle file describing the mappings.
    This uses a custom predicate `ex:mapsTo` to link database columns
    (represented as sh:path) to ontology terms.
    """
    g = Graph()

    # Define namespaces
    EX = Namespace("http://example.com/shacl-mappings#")
    DBP = Namespace("http://example.com/database-properties#") # For database column properties
    g.bind("sh", SH)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)
    g.bind("ex", EX)
    g.bind("dbp", DBP)
    # Note: We don't bind a specific ontology prefix here as ontology terms are full URIs

    # Define a NodeShape for the database table
    table_shape_uri = EX[f"{db_table_name}Shape"]
    g.add((table_shape_uri, RDF.type, SH.NodeShape))
    g.add((table_shape_uri, RDFS.label, Literal(f"SHACL Shape for {db_table_name}")))
    g.add((table_shape_uri, SH.targetClass, EX[db_table_name.replace('.', '_') + "Record"])) # A placeholder target class

    for db_column, ontology_term in mappings.items():
        # Create a blank node for the PropertyShape
        prop_shape = EX[f"{db_table_name.replace('.', '_')}_{db_column.replace('.', '_')}PropertyShape"]
        g.add((table_shape_uri, SH.property, prop_shape))
        g.add((prop_shape, RDF.type, SH.PropertyShape))

        # Define the path for the database column
        db_column_uri = DBP[db_column]
        g.add((prop_shape, SH.path, db_column_uri))

        # Add the custom mapping predicate
        g.add((prop_shape, EX.mapsTo, URIRef(ontology_term)))

        # Add a comment for clarity
        g.add((prop_shape, RDFS.comment, Literal(f"Maps database column '{db_column}' to ontology term '{ontology_term}'.")))

    return g.serialize(format='turtle')