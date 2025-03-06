import networkx as nx
from typing import Dict, Any
from ..core.logger import log_info, log_error

class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.metadata = {}

    def add_node(self, node_id: str, attributes: Dict[str, Any] = None):
        """Add a node to the knowledge graph with optional attributes."""
        try:
            self.graph.add_node(node_id, **attributes or {})
            log_info(f"Added node: {node_id}")
            return True
        except Exception as e:
            log_error(f"Error adding node {node_id}: {str(e)}")
            return False

    def add_edge(self, source: str, target: str, attributes: Dict[str, Any] = None):
        """Add an edge between two nodes with optional attributes."""
        try:
            self.graph.add_edge(source, target, **attributes or {})
            log_info(f"Added edge: {source} -> {target}")
            return True
        except Exception as e:
            log_error(f"Error adding edge {source} -> {target}: {str(e)}")
            return False

    def update_graph(self, data: Dict[str, Any]) -> bool:
        """Update the knowledge graph with new data."""
        try:
            for node, attributes in data.get('nodes', {}).items():
                self.add_node(node, attributes)
            
            for edge in data.get('edges', []):
                self.add_edge(edge['source'], edge['target'], edge.get('attributes'))
            
            self.metadata.update(data.get('metadata', {}))
            log_info("Graph updated successfully")
            return True
        except Exception as e:
            log_error(f"Error updating graph: {str(e)}")
            return False

    def get_subgraph(self, nodes):
        """Extract a subgraph containing specified nodes."""
        return self.graph.subgraph(nodes)

    def export_graph(self):
        """Export the graph data in a dictionary format."""
        return {
            'nodes': dict(self.graph.nodes(data=True)),
            'edges': [{'source': s, 'target': t, 'attributes': d} 
                     for s, t, d in self.graph.edges(data=True)],
            'metadata': self.metadata
        }