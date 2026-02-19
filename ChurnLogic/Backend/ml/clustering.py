"""Customer Behavior Clustering"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class CustomerClusterer:
    def __init__(self, n_clusters: int = 4):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(
            n_clusters=n_clusters,
            init='k-means++',
            random_state=42,
            n_init=10
        )
        self.scaler = StandardScaler()
        self.cluster_names = {
            0: 'Premium Loyalists',
            1: 'At-Risk Champions',
            2: 'Price Sensitive',
            3: 'Dormant Users'
        }
    
    def fit_predict(self, X: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Fit clustering model and predict"""
        logger.info(f"Clustering customers into {self.n_clusters} segments...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit and predict
        clusters = self.kmeans.fit_predict(X_scaled)
        
        # Calculate metrics
        inertia = self.kmeans.inertia_
        n_samples = X.shape[0]
        
        summary = {
            'n_clusters': self.n_clusters,
            'inertia': float(inertia),
            'cluster_sizes': np.bincount(clusters).tolist(),
            'silhouette_score': 0.0
        }
        
        logger.info(f"Clustering complete. Cluster distribution: {np.bincount(clusters)}")
        
        return clusters, summary
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict cluster for new data"""
        X_scaled = self.scaler.transform(X)
        return self.kmeans.predict(X_scaled)
    
    def get_cluster_profiles(
        self,
        X: np.ndarray,
        clusters: np.ndarray,
        df_original: pd.DataFrame
    ) -> Dict[int, Dict[str, Any]]:
        """Generate cluster profiles"""
        profiles = {}
        
        for cluster_id in range(self.n_clusters):
            mask = clusters == cluster_id
            cluster_data = df_original[mask]
            
            profile = {
                'cluster_id': cluster_id,
                'cluster_name': self.cluster_names.get(cluster_id, f'Cluster {cluster_id}'),
                'size': int(mask.sum()),
                'percentage': float(mask.sum() / len(clusters) * 100),
                'characteristics': {}
            }
            
            # Calculate characteristics
            for col in cluster_data.columns:
                if pd.api.types.is_numeric_dtype(cluster_data[col]):
                    profile['characteristics'][col] = {
                        'mean': float(cluster_data[col].mean()),
                        'median': float(cluster_data[col].median()),
                        'std': float(cluster_data[col].std())
                    }
            
            profiles[cluster_id] = profile
        
        return profiles
    
    def calculate_engagement_score(
        self,
        df: pd.DataFrame,
        clusters: np.ndarray
    ) -> np.ndarray:
        """Calculate engagement score per customer"""
        engagement_scores = np.zeros(len(df))
        
        factors = {
            'usage_frequency': 0.3,
            'monthly_charges': 0.2,
            'tenure': 0.25,
        }
        
        for col, weight in factors.items():
            if col in df.columns:
                col_min = df[col].min()
                col_max = df[col].max()
                if col_max > col_min:
                    normalized = (df[col] - col_min) / (col_max - col_min)
                    engagement_scores += normalized.values * weight
                else:
                    engagement_scores += weight
        
        return engagement_scores

clusterer = CustomerClusterer()