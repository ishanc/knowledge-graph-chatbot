from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDFS, XSD
from typing import Dict, Any
from ..core.logger import log_info, log_error

class RDFConverter:
    def __init__(self, graph):
        self.graph = graph
        self.rdf_graph = Graph()
        self.namespace = "http://example.org/kg/"

    def create_uri(self, entity: str) -> URIRef:
        """Create a URI for an entity."""
        return URIRef(f"{self.namespace}{entity}")

    def convert_to_rdf(self) -> Graph:
        """Convert the knowledge graph to RDF format."""
        try:
            graph_data = self.graph.export_graph()
            
            # Convert nodes
            for node_id, attributes in graph_data['nodes'].items():
                node_uri = self.create_uri(node_id)
                
                # Add node type
                node_type = attributes.get('type', 'Entity')
                self.rdf_graph.add((node_uri, RDF.type, self.create_uri(node_type)))
                
                # Add node attributes
                for key, value in attributes.items():
                    if key != 'type':
                        self.rdf_graph.add((
                            node_uri,
                            self.create_uri(key),
                            Literal(value)
                        ))

            # Convert edges
            for edge in graph_data['edges']:
                source_uri = self.create_uri(edge['source'])
                target_uri = self.create_uri(edge['target'])
                
                # Add relationship
                for key, value in edge.get('attributes', {}).items():
                    self.rdf_graph.add((
                        source_uri,
                        self.create_uri(key),
                        target_uri
                    ))

            log_info("Successfully converted graph to RDF")
            return self.rdf_graph

        except Exception as e:
            log_error(f"Error converting to RDF: {str(e)}")
            return None

    def save_to_file(self, file_path: str, format: str = 'turtle') -> bool:
        """Save the RDF graph to a file."""
        try:
            self.rdf_graph.serialize(destination=file_path, format=format)
            log_info(f"Successfully saved RDF to {file_path}")
            return True
        except Exception as e:
            log_error(f"Error saving RDF to file: {str(e)}")
            return False

    def load_from_file(self, file_path: str, format: str = 'turtle') -> bool:
        """Load RDF data from a file."""
        try:
            self.rdf_graph = Graph()
            self.rdf_graph.parse(file_path, format=format)
            log_info(f"Successfully loaded RDF from {file_path}")
            return True
        except Exception as e:
            log_error(f"Error loading RDF from file: {str(e)}")
            return False