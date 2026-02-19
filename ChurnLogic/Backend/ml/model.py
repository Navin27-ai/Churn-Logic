"""Churn Prediction Model"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import logging
from typing import Dict, Any, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class ChurnPredictionModel:
    def __init__(self):
        self.xgb_model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            random_state=42,
            n_jobs=-1
        )
        
        self.lr_model = LogisticRegression(
            max_iter=1000,
            random_state=42,
            n_jobs=-1
        )
        
        self.primary_model = self.xgb_model
        self.feature_names = None
        self.metrics = {}
        self.model_version = None
    
    def train(
        self,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: list,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Dict[str, Any]:
        """Train all models"""
        logger.info("Starting model training...")
        
        self.feature_names = feature_names
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
        
        # Train Random Forest
        logger.info("Training Random Forest...")
        self.xgb_model.fit(X_train, y_train)
        
        # Train Logistic Regression
        logger.info("Training Logistic Regression...")
        self.lr_model.fit(X_train, y_train)
        
        # Evaluate
        logger.info("Evaluating models...")
        metrics = self._evaluate_models(X_test, y_test)
        self.metrics = metrics
        
        self.model_version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info("Training complete!")
        return metrics
    
    def _evaluate_models(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Evaluate all models"""
        results = {}
        
        for name, model in [
            ('random_forest', self.xgb_model),
            ('logistic_regression', self.lr_model)
        ]:
            y_pred = model.predict(X_test)
            y_proba = model.predict_proba(X_test)[:, 1]
            
            results[name] = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1': f1_score(y_test, y_pred, zero_division=0),
                'roc_auc': roc_auc_score(y_test, y_proba)
            }
        
        results['primary_model'] = 'random_forest'
        results['xgboost'] = results['random_forest']
        
        logger.info(f"RF - Accuracy: {results['random_forest']['accuracy']:.4f}")
        
        return results
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict churn probability"""
        return self.primary_model.predict_proba(X)[:, 1]
    
    def predict_batch(self, X: np.ndarray) -> Dict[str, Any]:
        """Predict for batch of customers"""
        probabilities = self.predict(X)
        
        risk_levels = []
        for prob in probabilities:
            if prob > 0.7:
                risk_levels.append('HIGH')
            elif prob > 0.4:
                risk_levels.append('MEDIUM')
            else:
                risk_levels.append('LOW')
        
        return {
            'probabilities': probabilities.tolist(),
            'risk_levels': risk_levels,
            'count_high_risk': sum(1 for r in risk_levels if r == 'HIGH'),
            'count_medium_risk': sum(1 for r in risk_levels if r == 'MEDIUM'),
            'count_low_risk': sum(1 for r in risk_levels if r == 'LOW'),
            'average_probability': float(np.mean(probabilities))
        }
    
    def get_feature_importance(self) -> list:
        """Get feature importance from model"""
        if hasattr(self.primary_model, 'feature_importances_'):
            importance = self.primary_model.feature_importances_
            
            features_importance = [
                {
                    'feature': name,
                    'importance': float(imp)
                }
                for name, imp in zip(self.feature_names, importance)
            ]
            
            features_importance.sort(key=lambda x: x['importance'], reverse=True)
            
            return features_importance[:15]
        
        return []
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get model metrics"""
        return self.metrics

churn_model = ChurnPredictionModel()