"""SQLAlchemy Models"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(100), unique=True, index=True)
    dataset_id = Column(String(100), index=True)
    features = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(100), index=True)
    churn_probability = Column(Float)
    risk_level = Column(String(20))
    model_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Cluster(Base):
    __tablename__ = "clusters"
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(100), index=True)
    cluster_id = Column(Integer)
    cluster_name = Column(String(100))
    engagement_score = Column(Float)
    behavior_profile = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class SimulationResult(Base):
    __tablename__ = "simulation_results"
    id = Column(Integer, primary_key=True)
    scenario_name = Column(String(100))
    price_change = Column(Float)
    discount_percentage = Column(Float)
    campaign_type = Column(String(100))
    predicted_churn_change = Column(Float)
    revenue_impact = Column(Float)
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class CampaignRecommendation(Base):
    __tablename__ = "campaign_recommendations"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text)
    target_segment = Column(String(100))
    expected_impact = Column(Float)
    priority = Column(String(20))
    tags = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class ModelMetadata(Base):
    __tablename__ = "model_metadata"
    id = Column(Integer, primary_key=True)
    model_version = Column(String(50), unique=True)
    model_type = Column(String(50))
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    roc_auc = Column(Float)
    feature_names = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)