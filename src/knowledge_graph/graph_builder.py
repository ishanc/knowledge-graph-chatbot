from typing import Dict, Any
from ..core.logger import log_info, log_error
import uuid

class GraphBuilder:
    def __init__(self):
        self.knowledge_graph = {
            'nodes': {},
            'edges': [],
            'metadata': {}
        }

    def add_document(self, document_data: Dict[str, Any]) -> str:
        """Add document data to the knowledge graph."""
        try:
            doc_id = str(uuid.uuid4())
            
            # Create document node
            self.knowledge_graph['nodes'][doc_id] = {
                'type': 'document',
                'content': document_data.get('content', ''),
                **document_data.get('metadata', {})
            }

            # Handle structured data like tables
            if isinstance(document_data.get('content'), dict):
                for key, value in document_data['content'].items():
                    if key == 'tables':
                        self._process_tables(doc_id, value)
                    elif key == 'sheets':  # For Excel files
                        self._process_excel_sheets(doc_id, value)

            log_info(f"Added document to graph with ID: {doc_id}")
            return doc_id

        except Exception as e:
            log_error(f"Error adding document to graph: {str(e)}")
            return None

    def _process_tables(self, doc_id: str, tables: list):
        """Process table data and add to graph."""
        for idx, table in enumerate(tables):
            table_id = f"{doc_id}_table_{idx}"
            self.knowledge_graph['nodes'][table_id] = {
                'type': 'table',
                'content': table
            }
            self.knowledge_graph['edges'].append({
                'source': doc_id,
                'target': table_id,
                'attributes': {'type': 'has_table'}
            })

    def _process_excel_sheets(self, doc_id: str, sheets: Dict[str, Any]):
        """Process Excel sheets and add to graph."""
        for sheet_name, data in sheets.items():
            sheet_id = f"{doc_id}_sheet_{sheet_name}"
            self.knowledge_graph['nodes'][sheet_id] = {
                'type': 'sheet',
                'content': data,
                'sheet_name': sheet_name
            }
            self.knowledge_graph['edges'].append({
                'source': doc_id,
                'target': sheet_id,
                'attributes': {'type': 'has_sheet'}
            })

    def get_graph(self) -> Dict[str, Any]:
        """Get the current state of the knowledge graph."""
        return self.knowledge_graph

    def clear_graph(self):
        """Clear the knowledge graph."""
        self.knowledge_graph = {
            'nodes': {},
            'edges': [],
            'metadata': {}
        }