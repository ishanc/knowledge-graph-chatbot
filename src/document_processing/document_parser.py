import os
from typing import Dict, Any, Optional
from .pdf_processor import PDFProcessor
from .excel_processor import ExcelProcessor
from .csv_processor import CSVProcessor
from .docx_processor import DocxProcessor
from .image_processor import ImageProcessor
from ..core.logger import log_info, log_error
from ..core.config import ALLOWED_EXTENSIONS

class DocumentParser:
    def __init__(self):
        self.processors = {
            'pdf': PDFProcessor,
            'xlsx': ExcelProcessor,
            'xls': ExcelProcessor,
            'csv': CSVProcessor,
            'docx': DocxProcessor,
            'jpg': ImageProcessor,
            'jpeg': ImageProcessor,
            'png': ImageProcessor
        }

    def get_file_extension(self, filename: str) -> str:
        """Extract file extension from filename."""
        return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    def validate_file(self, filename: str) -> bool:
        """Validate if the file type is supported."""
        extension = self.get_file_extension(filename)
        return extension in ALLOWED_EXTENSIONS

    def parse(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Parse the document and extract structured data."""
        try:
            if not self.validate_file(file_path):
                raise ValueError(f"Unsupported file type: {file_path}")

            extension = self.get_file_extension(file_path)
            processor_class = self.processors.get(extension)
            
            if not processor_class:
                raise ValueError(f"No processor found for extension: {extension}")

            processor = processor_class(file_path)
            extracted_data = processor.extract_data()
            
            log_info(f"Successfully parsed document: {file_path}")
            return {
                'content': extracted_data,
                'metadata': {
                    'file_type': extension,
                    'file_path': file_path,
                    'timestamp': os.path.getmtime(file_path)
                }
            }

        except Exception as e:
            log_error(f"Error parsing document {file_path}: {str(e)}")
            return None

    def extract_data(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Extract and preprocess data from document."""
        try:
            parsed_data = self.parse(file_path)
            if not parsed_data:
                return None

            # Get file type and content
            file_type = self.get_file_extension(file_path)
            content = parsed_data['content']

            # Structure the data based on file type
            structured_data = {
                'content': content,
                'metadata': {
                    'file_type': file_type,
                    'file_path': file_path,
                    'timestamp': os.path.getmtime(file_path),
                    **parsed_data.get('metadata', {})
                }
            }

            # Additional processing for specific file types
            if file_type in ['xlsx', 'xls']:
                structured_data['relationships'] = parsed_data.get('relationships', [])
            elif file_type in ['jpg', 'jpeg', 'png']:
                structured_data['metadata']['image_info'] = parsed_data.get('image_info', {})

            log_info(f"Successfully processed document: {file_path}")
            return structured_data

        except Exception as e:
            log_error(f"Error extracting data from {file_path}: {str(e)}")
            return None