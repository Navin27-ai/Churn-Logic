# ChurnLogic — Setup & Run Guide

AI-powered customer retention intelligence platform. Upload your customer data to predict churn, analyze behavior, simulate campaigns, and get AI-generated retention strategies.

---

## Requirements

Make sure you have these installed before starting:

- Python 3.9 or higher → https://www.python.org/downloads/
- pip (comes with Python)

---

## Folder Structure

```
ChurnLogic/
├── Backend/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   └── requirements.txt
├── Frontend/
│   └── index.html
└── customers.csv (sample data)
```

---

## Step 1 — Install Backend Dependencies

Open a terminal and run:

```bash
cd A:\ChurnLogic\Backend
pip install fastapi uvicorn pandas python-multipart
```

---

## Step 2 — Start the Backend

In the same terminal:

```bash
uvicorn main:app --reload
```

You should see:
```
INFO: Uvicorn running on http://127.0.0.1:8000
```

Keep this terminal open the whole time.

---

## Step 3 — Open the Frontend

Open File Explorer and navigate to:
```
A:\ChurnLogic\Frontend\
```

Double-click **index.html** to open it in your browser.

---

## Step 4 — Upload Your Data

1. Click **Upload Data** in the sidebar
2. Select your CSV file
3. Click **Start Upload and Processing**
4. You'll be redirected to the Dashboard automatically

---

## CSV File Format

Your CSV must contain these exact column names:

| Column | Description |
|---|---|
| `customer_id` | Unique ID for each customer |
| `tenure` | How many months they've been a customer |
| `monthly_charges` | How much they pay per month |
| `total_charges` | Total amount paid overall |
| `churn` | 1 = churned (left), 0 = still active |

Sample files included:
- `customers_50.csv` — 50 customers
- `customers_100.csv` — 100 customers

---

## Pages Overview

| Page | What it does |
|---|---|
| **Dashboard** | Overview of churn rate, at-risk customers, charts |
| **Upload Data** | Upload a new CSV file |
| **Churn Analysis** | Full customer table with risk levels and filters |
| **Behavior Analytics** | Customers grouped by spending with churn rates |
| **Simulation Studio** | Test discount campaigns and see revenue impact |
| **AI Strategy** | 6 AI-generated retention strategies |
| **Insights** | Plain-English observations from your data |

---

## Restarting After Closing

Every time you close the terminal, the backend stops. To restart:

**Terminal 1 — Backend:**
```bash
cd A:\ChurnLogic\Backend
uvicorn main:app --reload
```

**Then re-upload your CSV** — data is stored in memory, so it resets when the backend restarts.

---

## Common Issues

**"Upload failed" error**
- Make sure the backend is running in the terminal before uploading

**Charts are empty after upload**
- Refresh the page and upload your CSV again

**Backend won't start**
- Make sure you're in the correct folder: `A:\ChurnLogic\Backend`
- Make sure all packages are installed: `pip install fastapi uvicorn pandas python-multipart`

---

## Built With

- **Frontend** — HTML, Tailwind CSS, Chart.js
- **Backend** — Python, FastAPI, Pandas

---

*ChurnLogic — Built to help businesses understand and reduce customer churn.*