import unittest
import os
from src.document_processing.document_parser import DocumentParser
from src.document_processing.pdf_processor import PDFProcessor
from src.document_processing.excel_processor import ExcelProcessor
from src.document_processing.csv_processor import CSVProcessor
from src.document_processing.docx_processor import DocxProcessor
from src.document_processing.image_processor import ImageProcessor

class TestDocumentProcessing(unittest.TestCase):
    def setUp(self):
        self.test_files_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        os.makedirs(self.test_files_dir, exist_ok=True)
        self.document_parser = DocumentParser()

    def test_file_extension_validation(self):
        valid_files = ['test.pdf', 'test.xlsx', 'test.csv', 'test.docx', 'test.jpg']
        invalid_files = ['test.exe', 'test.py', 'test']
        
        for file in valid_files:
            self.assertTrue(self.document_parser.validate_file(file))
        
        for file in invalid_files:
            self.assertFalse(self.document_parser.validate_file(file))

    def test_pdf_processor(self):
        processor = PDFProcessor("test.pdf")
        self.assertIsNotNone(processor)

    def test_excel_processor(self):
        processor = ExcelProcessor("test.xlsx")
        self.assertIsNotNone(processor)

    def test_csv_processor(self):
        processor = CSVProcessor("test.csv")
        self.assertIsNotNone(processor)

    def test_docx_processor(self):
        processor = DocxProcessor("test.docx")
        self.assertIsNotNone(processor)

    def test_image_processor(self):
        processor = ImageProcessor("test.jpg")
        self.assertIsNotNone(processor)

if __name__ == '__main__':
    unittest.main()