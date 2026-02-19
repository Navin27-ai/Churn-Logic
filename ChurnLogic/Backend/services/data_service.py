"""Data Service"""
import pandas as pd
import logging
from typing import Dict, Any
import io

logger = logging.getLogger(__name__)

class DataService:
    @staticmethod
    async def process_upload(file, db) -> Dict[str, Any]:
        try:
            contents = await file.read()
            df = pd.read_csv(io.BytesIO(contents))
            
            return {
                'status': 'success',
                'dataset_id': 'test_123',
                'rows': len(df),
                'columns': len(df.columns),
                'preview': df.head(5).to_dict(orient='records'),
                'validation_results': {
                    'total_rows': len(df),
                    'total_columns': len(df.columns),
                    'columns': df.columns.tolist(),
                    'warnings': []
                }
            }
        except Exception as e:
            logger.error(f"Upload error: {e}")
            raise

    @staticmethod
    def validate_data(df):
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': df.columns.tolist(),
            'warnings': []
        }

    @staticmethod
    def get_target_variable(df):
        churn_col = None
        for col in df.columns:
            if col.lower() in ['churn', 'churned', 'has_churn']:
                churn_col = col
                break
        
        if churn_col is None:
            raise ValueError("No churn column found")
        
        return df[churn_col].astype(int), churn_col

data_service = DataService()