from flask import Blueprint, request, jsonify
from ..core.config import ALLOWED_EXTENSIONS
from ..document_processing.document_parser import DocumentParser
from ..knowledge_graph.graph_builder import GraphBuilder
from ..vector_db.vectorizer import Vectorizer
from ..llm.mistral_client import MistralClient
from ..core.logger import log_info, log_error
import os

api = Blueprint('api', __name__)
document_parser = DocumentParser()
graph_builder = GraphBuilder()
vectorizer = Vectorizer()

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200

@api.route('/documents', methods=['POST'])
def upload_document():
    """Handle document upload and processing."""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if not document_parser.validate_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400

        # Process the document
        result = document_parser.extract_data(file)
        if not result:
            return jsonify({'error': 'Failed to process document'}), 500

        # Update knowledge graph
        doc_id = graph_builder.add_document(result)
        if not doc_id:
            return jsonify({'error': 'Failed to add to knowledge graph'}), 500

        # Update vector database
        if not vectorizer.convert_to_vector(graph_builder.get_graph()):
            return jsonify({'error': 'Failed to update vector database'}), 500

        return jsonify({
            'message': 'Document processed successfully',
            'document_id': doc_id
        }), 201

    except Exception as e:
        log_error(f"Error in upload_document: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/query', methods=['POST'])
def query_knowledge():
    """Query the knowledge graph."""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400

        # Get similar nodes from vector database
        similar_nodes = vectorizer.get_similar_nodes(data['query'])
        
        # Get context from similar nodes
        context = []
        for node_id, score in similar_nodes:
            node_info = graph_builder.get_graph()['nodes'].get(node_id, {})
            context.append({
                'node_id': node_id,
                'similarity': score,
                'info': node_info
            })

        return jsonify({
            'results': context
        }), 200

    except Exception as e:
        log_error(f"Error in query_knowledge: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api.route('/graph', methods=['GET'])
def get_graph():
    """Get the current state of the knowledge graph."""
    try:
        return jsonify(graph_builder.get_graph()), 200
    except Exception as e:
        log_error(f"Error in get_graph: {str(e)}")
        return jsonify({'error': str(e)}), 500