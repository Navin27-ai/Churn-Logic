"""Pydantic Models"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class UploadResponse(BaseModel):
    status: str
    dataset_id: str
    rows: int
    columns: int
    preview: List[Dict[str, Any]]
    validation_results: Dict[str, Any]

class PredictionResponse(BaseModel):
    predictions: List[Dict[str, Any]]

class ClusterResponse(BaseModel):
    clusters: List[Dict[str, Any]]

class SimulationRequest(BaseModel):
    price_change: float
    discount_percentage: float
    campaign_intervention: bool
    campaign_type: Optional[str] = None

class SimulationResponse(BaseModel):
    predicted_churn_change: float
    revenue_impact: float
    scenario_comparison: Dict[str, Any]