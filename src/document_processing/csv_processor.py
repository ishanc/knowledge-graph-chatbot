import pandas as pd
from typing import Dict, Any
from ..core.logger import log_info, log_error

class CSVProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_data(self) -> Dict[str, Any]:
        """Extract data from CSV file."""
        try:
            df = pd.read_csv(self.file_path)
            
            # Get basic statistics
            stats = {
                'row_count': len(df),
                'column_count': len(df.columns),
                'columns': df.columns.tolist(),
                'missing_values': df.isnull().sum().to_dict()
            }

            return {
                'content': df.to_dict(orient='records'),
                'metadata': {
                    'statistics': stats,
                    'type': 'csv'
                }
            }

        except Exception as e:
            log_error(f"Error processing CSV {self.file_path}: {str(e)}")
            return {'content': [], 'metadata': {'type': 'csv'}}