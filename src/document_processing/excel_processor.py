import pandas as pd
from typing import Dict, Any, List
from ..core.logger import log_info, log_error

class ExcelProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_data(self) -> Dict[str, Any]:
        """Extract data and relationships from Excel file."""
        try:
            excel_data = pd.read_excel(self.file_path, sheet_name=None)
            sheets_data = {}
            relationships = []

            for sheet_name, df in excel_data.items():
                # Convert DataFrame to dict format
                sheet_data = df.to_dict(orient='records')
                sheets_data[sheet_name] = sheet_data

                # Extract column relationships
                columns = df.columns.tolist()
                for i, col1 in enumerate(columns):
                    for col2 in columns[i+1:]:
                        relationships.append({
                            'source': col1,
                            'target': col2,
                            'type': 'column_relationship',
                            'sheet': sheet_name
                        })

            return {
                'sheets': sheets_data,
                'relationships': relationships,
                'metadata': {
                    'num_sheets': len(sheets_data),
                    'sheet_names': list(sheets_data.keys())
                }
            }

        except Exception as e:
            log_error(f"Error processing Excel file {self.file_path}: {str(e)}")
            return {'sheets': {}, 'relationships': [], 'metadata': {}}