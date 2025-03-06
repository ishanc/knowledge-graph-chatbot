# Knowledge Graph Chatbot

An advanced document processing and chatbot system that leverages knowledge graphs, vector embeddings, and the Hugging Face Mistral model for intelligent responses.

## Features

- Upload documents in PDF, XLSX, CSV, DOCX, and image formats.
- Retain row and column relationships in XLSX files.
- Build and update a knowledge graph based on uploaded documents.
- Convert the knowledge graph into RDF format.
- Store the knowledge graph in a vector database.
- Retrieve information using a retrieval system.
- Utilize Mistral for inference through Hugging Face.

## System Architecture

### Core Components

```
knowledge-graph-chatbot/
├── src/
│   ├── core/                  # Core configurations and utilities
│   │   ├── config.py         # Application configuration
│   │   └── logger.py         # Logging setup
│   ├── document_processing/   # Document handling
│   │   ├── document_parser.py # Main parser interface
│   │   ├── pdf_processor.py  # PDF processing
│   │   ├── excel_processor.py # Excel processing with relation preservation
│   │   ├── csv_processor.py  # CSV processing
│   │   ├── docx_processor.py # Word document processing
│   │   └── image_processor.py # Image processing with OCR
│   ├── knowledge_graph/      # Knowledge graph operations
│   ├── vector_db/           # Vector database operations
│   ├── llm/                 # Language model integration
│   └── api/                 # RESTful API endpoints
└── ui/
    ├── chat/               # Chat interface
    └── admin/             # Admin interface for document management
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 13+ (optional)
- Tesseract OCR

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/knowledge-graph-chatbot.git
cd knowledge-graph-chatbot
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.template .env
# Edit .env with your configurations
```

### Frontend Setup

1. Chat UI Setup:
```bash
cd ui/chat
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

2. Admin UI Setup:
```bash
cd ui/admin
npm create vite@latest . -- --template react-ts
npm install
npm run dev
```

## Configuration

### Environment Variables
```env
HF_API_KEY=your_huggingface_api_key
HF_MODEL_ID=mistralai/Mistral-7B-Instruct-v0.1
FLASK_ENV=development
FLASK_DEBUG=1
```

### Supported File Types
- PDF (.pdf)
- Excel (.xlsx, .xls)
- Word (.docx)
- CSV (.csv)
- Images (.jpg, .jpeg, .png)

## API Reference

### Document Processing

#### Upload Document
```http
POST /api/documents
Content-Type: multipart/form-data

file: <document>
```

Response:
```json
{
    "message": "Document processed successfully",
    "document_id": "uuid"
}
```

#### Query Knowledge Base
```http
POST /api/query
Content-Type: application/json

{
    "query": "Your question here"
}
```

Response:
```json
{
    "response": "Generated answer",
    "context": [
        {
            "node_id": "uuid",
            "similarity": 0.95,
            "info": {
                "type": "document",
                "content": "..."
            }
        }
    ]
}
```

### Knowledge Graph Operations

#### Get Graph State
```http
GET /api/graph
```

Response:
```json
{
    "nodes": [...],
    "edges": [...],
    "metadata": {...}
}
```

## User Interfaces

### Chat Interface
- Multiple chat sessions
- Context-aware conversations
- Session management
- User authentication
- Message history

### Admin Interface
- Drag-and-drop file upload
- Knowledge graph visualization
- Processing status tracking
- Document management
- Graph exploration

## Testing

### Running Tests
```bash
# Run all tests
python -m unittest discover tests

# Run specific test suite
python -m unittest tests/test_document_processing.py
python -m unittest tests/test_knowledge_graph.py
python -m unittest tests/test_vector_db.py
python -m unittest tests/test_llm.py
```

### Test Coverage
```bash
coverage run -m unittest discover
coverage report
coverage html  # Generates HTML report
```

## Performance Considerations

### Limitations
- Maximum file size: 16MB
- Vector dimension: 384
- Supported image formats: JPG, PNG
- Rate limits: 100 requests/minute

### Optimization Tips
- Use batch processing for multiple files
- Enable caching for frequent queries
- Implement pagination for large datasets
- Use appropriate indexes for database queries

## Security

### API Security
- API key authentication
- Rate limiting
- Input validation
- File type verification
- Size restrictions

### Data Security
- Encrypted storage
- Secure file handling
- Session management
- Access control

## Troubleshooting

### Common Issues
1. File upload failures
   - Check file size
   - Verify file type
   - Check permissions

2. Processing errors
   - Check log files
   - Verify dependencies
   - Check API keys

3. Performance issues
   - Monitor memory usage
   - Check database connections
   - Review cache settings

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for frontend
- Write unit tests
- Document new features
- Update README as needed

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues
- Documentation Wiki
- Community Forum