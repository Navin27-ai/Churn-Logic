"""Data Preprocessing"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from typing import Tuple, Dict, Any

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.imputer = SimpleImputer(strategy='median')
        self.feature_names = None
        self.categorical_features = []
        self.numerical_features = []
    
    def detect_feature_types(self, df: pd.DataFrame) -> Dict[str, list]:
        """Detect feature types in dataset"""
        numerical = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical = df.select_dtypes(include=['object']).columns.tolist()
        
        self.numerical_features = numerical
        self.categorical_features = categorical
        
        return {
            'numerical': numerical,
            'categorical': categorical,
            'total_features': len(numerical) + len(categorical)
        }
    
    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values"""
        # Numerical: median imputation
        for col in self.numerical_features:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
        
        # Categorical: mode imputation
        for col in self.categorical_features:
            if df[col].isnull().any():
                mode_val = df[col].mode()[0]
                df[col].fillna(mode_val, inplace=True)
        
        return df
    
    def encode_categorical(self, df: pd.DataFrame, fit: bool = False) -> pd.DataFrame:
        """Encode categorical variables"""
        df_encoded = df.copy()
        
        for col in self.categorical_features:
            if col not in df_encoded.columns:
                continue
                
            if fit:
                le = LabelEncoder()
                df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
                self.label_encoders[col] = le
            else:
                if col in self.label_encoders:
                    le = self.label_encoders[col]
                    df_encoded[col] = le.transform(df_encoded[col].astype(str))
        
        return df_encoded
    
    def scale_features(self, X: pd.DataFrame, fit: bool = False) -> np.ndarray:
        """Scale numerical features"""
        X_numerical = X[self.numerical_features].copy()
        
        if fit:
            X_scaled = self.scaler.fit_transform(X_numerical)
        else:
            X_scaled = self.scaler.transform(X_numerical)
        
        return X_scaled
    
    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create engineered features"""
        df_eng = df.copy()
        
        # Tenure-based features
        if 'tenure' in df_eng.columns:
            df_eng['tenure_squared'] = df_eng['tenure'] ** 2
            df_eng['tenure_log'] = np.log1p(df_eng['tenure'])
        
        # Contract-related features
        if 'monthly_charges' in df_eng.columns and 'total_charges' in df_eng.columns:
            df_eng['charges_ratio'] = (
                df_eng['monthly_charges'] / (df_eng['total_charges'] + 1)
            )
        
        return df_eng
    
    def fit_transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, list]:
        """Fit preprocessor and transform data"""
        # Detect feature types
        self.detect_feature_types(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Engineer features
        df = self.engineer_features(df)
        
        # Encode categorical
        df = self.encode_categorical(df, fit=True)
        
        # Scale features
        X = self.scale_features(df, fit=True)
        
        self.feature_names = df.columns.tolist()
        
        return X, self.feature_names
    
    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transform new data using fitted preprocessor"""
        df = self.handle_missing_values(df)
        df = self.engineer_features(df)
        df = self.encode_categorical(df, fit=False)
        X = self.scale_features(df, fit=False)
        
        return X

preprocessor = DataPreprocessor()