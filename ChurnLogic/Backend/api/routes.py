"""API Routes"""
from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router = APIRouter()
app_data = {"df": None}

def get_col(df, candidates):
    return next((c for c in candidates if c in df.columns), None)

@router.get("/test")
async def test():
    return {"message": "API working"}

@router.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        app_data["df"] = df
        return {"status": "success", "rows": len(df), "columns": len(df.columns), "preview": df.head(5).to_dict(orient="records")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/dashboard-data")
async def get_dashboard_data():
    if app_data["df"] is None:
        return {"total_customers": 0, "churn_rate": 0.0, "at_risk": 0, "avg_score": 0.0, "avg_monthly_charge": 0.0, "churn_distribution": [], "retention_by_segment": [], "behavior_segments": []}

    df = app_data["df"].copy()
    total = len(df)
    churn_col = get_col(df, ["churn","Churn","CHURN","churn_status","Churn_Status"])
    charge_col = get_col(df, ["monthly_charges","MonthlyCharges","monthly_charge"])
    tenure_col = get_col(df, ["tenure","Tenure","TENURE"])

    if churn_col:
        df[churn_col] = pd.to_numeric(df[churn_col], errors='coerce').fillna(0)
        churn_rate = float(df[churn_col].mean() * 100)
        at_risk = int(df[churn_col].sum())
    else:
        churn_rate, at_risk = 0.0, 0

    avg_charge = float(pd.to_numeric(df[charge_col], errors='coerce').mean()) if charge_col else 0.0

    retention_by_segment = []
    if tenure_col and churn_col:
        df[tenure_col] = pd.to_numeric(df[tenure_col], errors='coerce').fillna(0)
        df["_seg"] = pd.cut(df[tenure_col], bins=[0,6,12,24,9999], labels=["New (0-6m)","Growing (6-12m)","Established (1-2y)","Loyal (2y+)"])
        for seg, grp in df.groupby("_seg", observed=True):
            if len(grp) > 0:
                retention_by_segment.append({"segment": str(seg), "retention_rate": round((1 - grp[churn_col].mean()) * 100, 1), "count": len(grp)})

    behavior_segments = []
    if charge_col:
        df[charge_col] = pd.to_numeric(df[charge_col], errors='coerce').fillna(0)
        df["_beh"] = pd.cut(df[charge_col], bins=[0,40,70,90,9999], labels=["Budget","Standard","Premium","Enterprise"])
        for seg, grp in df.groupby("_beh", observed=True):
            if len(grp) > 0:
                behavior_segments.append({"segment": str(seg), "count": len(grp)})

    return {
        "total_customers": total, "churn_rate": round(churn_rate, 1),
        "at_risk": at_risk, "avg_score": round(churn_rate / 100, 2),
        "avg_monthly_charge": round(avg_charge, 2),
        "churn_distribution": [{"label": "Churned", "value": at_risk}, {"label": "Retained", "value": total - at_risk}],
        "retention_by_segment": retention_by_segment,
        "behavior_segments": behavior_segments
    }

@router.get("/churn-analysis")
async def get_churn_analysis():
    if app_data["df"] is None:
        return {"status": "no_data", "customers": []}
    df = app_data["df"].copy()
    churn_col = get_col(df, ["churn","Churn","CHURN","churn_status","Churn_Status"])
    charge_col = get_col(df, ["monthly_charges","MonthlyCharges","monthly_charge"])
    tenure_col = get_col(df, ["tenure","Tenure","TENURE"])
    id_col = get_col(df, ["customer_id","CustomerID","customer_id","id","ID"])

    if churn_col:
        df[churn_col] = pd.to_numeric(df[churn_col], errors='coerce').fillna(0)
    if charge_col:
        df[charge_col] = pd.to_numeric(df[charge_col], errors='coerce').fillna(0)
    if tenure_col:
        df[tenure_col] = pd.to_numeric(df[tenure_col], errors='coerce').fillna(0)

    customers = []
    for _, row in df.iterrows():
        cid = str(row[id_col]) if id_col else f"CUST-{_}"
        churn = int(row[churn_col]) if churn_col else 0
        charge = float(row[charge_col]) if charge_col else 0.0
        tenure = int(row[tenure_col]) if tenure_col else 0
        risk = "High" if churn == 1 else ("Medium" if charge > 70 else "Low")
        customers.append({"id": cid, "tenure": tenure, "monthly_charge": charge, "churn": churn, "risk": risk})

    churned = [c for c in customers if c["churn"] == 1]
    retained = [c for c in customers if c["churn"] == 0]
    return {"status": "ok", "total": len(customers), "churned": len(churned), "retained": len(retained), "churn_rate": round(len(churned)/len(customers)*100, 1) if customers else 0, "customers": customers}

@router.get("/behavior-analytics")
async def get_behavior_analytics():
    if app_data["df"] is None:
        return {"status": "no_data", "segments": []}
    df = app_data["df"].copy()
    churn_col = get_col(df, ["churn","Churn","CHURN"])
    charge_col = get_col(df, ["monthly_charges","MonthlyCharges","monthly_charge"])
    tenure_col = get_col(df, ["tenure","Tenure","TENURE"])

    if charge_col:
        df[charge_col] = pd.to_numeric(df[charge_col], errors='coerce').fillna(0)
    if churn_col:
        df[churn_col] = pd.to_numeric(df[churn_col], errors='coerce').fillna(0)
    if tenure_col:
        df[tenure_col] = pd.to_numeric(df[tenure_col], errors='coerce').fillna(0)

    segments = []
    if charge_col:
        df["_beh"] = pd.cut(df[charge_col], bins=[0,40,70,90,9999], labels=["Budget ($0-40)","Standard ($40-70)","Premium ($70-90)","Enterprise ($90+)"])
        for seg, grp in df.groupby("_beh", observed=True):
            if len(grp) > 0:
                churn_rate = round(grp[churn_col].mean() * 100, 1) if churn_col else 0
                avg_charge = round(grp[charge_col].mean(), 2)
                avg_tenure = round(grp[tenure_col].mean(), 1) if tenure_col else 0
                segments.append({"segment": str(seg), "count": len(grp), "churn_rate": churn_rate, "avg_charge": avg_charge, "avg_tenure": avg_tenure})

    return {"status": "ok", "segments": segments}

@router.post("/train-model")
async def train_model():
    return {"status": "success"}

@router.post("/predict-churn")
async def predict_churn():
    return {"predictions": []}

@router.get("/model-metrics")
async def get_model_metrics():
    return {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1_score": 0.0, "roc_auc": 0.0}

@router.get("/feature-importance")
async def get_feature_importance():
    return []

@router.post("/cluster-users")
async def cluster_users():
    return {"clusters": []}

@router.get("/cluster-summary")
async def get_cluster_summary():
    return {}

@router.post("/simulate-scenario")
async def simulate_scenario():
    return {"predicted_churn_change": 0.0, "revenue_impact": 0.0}

@router.post("/generate-retention-strategy")
async def generate_retention_strategy():
    return {"strategies": []}

@router.get("/behavior-segments")
async def get_behavior_segments():
    return {"segments": []}

@router.get("/insights")
async def get_insights():
    return {"insights": []}