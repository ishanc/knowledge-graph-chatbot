import unittest
from src.knowledge_graph.graph_builder import GraphBuilder
from src.knowledge_graph.rdf_converter import RDFConverter
from src.knowledge_graph.graph_manager import GraphManager

class TestKnowledgeGraph(unittest.TestCase):

    def setUp(self):
        self.graph_builder = GraphBuilder()
        self.rdf_converter = RDFConverter()
        self.graph_manager = GraphManager()

    def test_graph_builder_initialization(self):
        self.assertIsNotNone(self.graph_builder)

    def test_graph_manager_initialization(self):
        self.assertIsNotNone(self.graph_manager)

    def test_rdf_converter_initialization(self):
        self.assertIsNotNone(self.rdf_converter)

    def test_add_document_to_graph(self):
        # Assuming add_document is a method in GraphBuilder
        result = self.graph_builder.add_document("sample_document")
        self.assertTrue(result)

    def test_convert_graph_to_rdf(self):
        # Assuming convert_to_rdf is a method in RDFConverter
        rdf_output = self.rdf_converter.convert_to_rdf()
        self.assertIsInstance(rdf_output, str)

    def test_graph_manager_update(self):
        # Assuming update_graph is a method in GraphManager
        update_result = self.graph_manager.update_graph()
        self.assertTrue(update_result)

if __name__ == '__main__':
    unittest.main()