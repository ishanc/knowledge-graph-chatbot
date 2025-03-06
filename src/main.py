from flask import Flask, request, jsonify
from core.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, HF_API_KEY, HF_MODEL_ID
from core.logger import log_info, log_error
from document_processing.document_parser import DocumentParser
from knowledge_graph.graph_builder import GraphBuilder
from knowledge_graph.rdf_converter import RDFConverter
from vector_db.vectorizer import Vectorizer
from vector_db.retriever import Retriever
from llm.mistral_client import MistralClient
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize components
document_parser = DocumentParser()
graph_builder = GraphBuilder()
vectorizer = Vectorizer()
retriever = Retriever(vectorizer)
mistral_client = MistralClient(
    api_key=os.getenv('HF_API_KEY', HF_API_KEY),
    model_id=os.getenv('HF_MODEL_ID', HF_MODEL_ID)
)

@app.route('/upload', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not document_parser.validate_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Save and process file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Parse document
        parsed_data = document_parser.extract_data(file_path)
        if not parsed_data:
            return jsonify({'error': 'Failed to parse document'}), 500

        # Update knowledge graph
        graph_builder.update_graph(parsed_data)
        
        # Update vector database
        vectorizer.convert_to_vector(graph_builder.get_graph())

        return jsonify({'message': 'Document processed successfully'}), 200

    except Exception as e:
        log_error(f"Error processing upload: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['POST'])
def query_knowledge_base():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400

    try:
        # Get similar nodes from vector database
        similar_nodes = retriever.get_similar_nodes(data['query'])
        
        # Get context from similar nodes
        context = []
        for node_id, score in similar_nodes:
            node_info = retriever.get_node_info(node_id)
            context.append({
                'node_id': node_id,
                'similarity': score,
                'info': node_info
            })

        # Generate response using Mistral
        response = mistral_client.query(
            prompt=f"Query: {data['query']}\nContext: {context}"
        )

        return jsonify({
            'response': response,
            'context': context
        }), 200

    except Exception as e:
        log_error(f"Error processing query: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)