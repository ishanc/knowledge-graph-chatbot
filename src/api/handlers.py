from typing import Dict, Any, Optional
from ..core.logger import log_info, log_error
from ..document_processing.document_parser import DocumentParser
from ..knowledge_graph.graph_builder import GraphBuilder
from ..vector_db.vectorizer import Vectorizer
from ..llm.mistral_client import MistralClient
import os

class APIHandler:
    def __init__(self):
        self.document_parser = DocumentParser()
        self.graph_builder = GraphBuilder()
        self.vectorizer = Vectorizer()
        self.mistral_client = MistralClient()

    def process_document(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Process a document and update all necessary components."""
        try:
            # Parse document
            parsed_data = self.document_parser.extract_data(file_path)
            if not parsed_data:
                log_error(f"Failed to parse document: {file_path}")
                return None

            # Add to knowledge graph
            doc_id = self.graph_builder.add_document(parsed_data)
            if not doc_id:
                log_error("Failed to add document to knowledge graph")
                return None

            # Update vector database
            if not self.vectorizer.convert_to_vector(self.graph_builder.get_graph()):
                log_error("Failed to update vector database")
                return None

            return {
                'document_id': doc_id,
                'parsed_data': parsed_data
            }

        except Exception as e:
            log_error(f"Error in process_document: {str(e)}")
            return None

    def query_knowledge_base(self, query: str, max_results: int = 5) -> Optional[Dict[str, Any]]:
        """Query the knowledge base and get relevant information."""
        try:
            # Get similar nodes
            similar_nodes = self.vectorizer.get_similar_nodes(query, max_results)
            
            # Get context from similar nodes
            context = []
            for node_id, score in similar_nodes:
                node_info = self.graph_builder.get_graph()['nodes'].get(node_id, {})
                context.append({
                    'node_id': node_id,
                    'similarity': score,
                    'info': node_info
                })

            # Generate response using LLM
            llm_response = self.mistral_client.query(
                prompt=f"Query: {query}\nContext: {context}"
            )

            return {
                'response': llm_response,
                'context': context
            }

        except Exception as e:
            log_error(f"Error in query_knowledge_base: {str(e)}")
            return None

    def get_graph_state(self) -> Optional[Dict[str, Any]]:
        """Get the current state of the knowledge graph."""
        try:
            return self.graph_builder.get_graph()
        except Exception as e:
            log_error(f"Error in get_graph_state: {str(e)}")
            return None