import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
HF_API_KEY = os.getenv('HF_API_KEY', '<your-huggingface-api-key>')
HF_MODEL_ID = os.getenv('HF_MODEL_ID', 'mistralai/Mistral-7B-Instruct-v0.1')
HF_API_BASE = "https://api-inference.huggingface.co/models/"

# File Upload Configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads/")
ALLOWED_EXTENSIONS = {'pdf', 'xlsx', 'csv', 'docx', 'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for uploads

# Vector DB Configuration
VECTOR_DIMENSION = 384  # Dimension for sentence-transformers model
SIMILARITY_THRESHOLD = 0.7

# Logging Configuration
LOG_LEVEL = 'DEBUG'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'