# src/document_processing/image_processor.py

from PIL import Image
import pytesseract
from typing import Dict, Any
from ..core.logger import log_info, log_error

class ImageProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_data(self) -> Dict[str, Any]:
        """Extract text and metadata from image."""
        try:
            image = Image.open(self.file_path)
            
            # Extract text using OCR
            text = pytesseract.image_to_string(image)
            
            # Get image metadata
            metadata = {
                'format': image.format,
                'size': image.size,
                'mode': image.mode,
                'info': image.info,
                'type': 'image'
            }

            return {
                'content': text.strip(),
                'metadata': metadata
            }

        except Exception as e:
            log_error(f"Error processing image {self.file_path}: {str(e)}")
            return {
                'content': '',
                'metadata': {'type': 'image'}
            }