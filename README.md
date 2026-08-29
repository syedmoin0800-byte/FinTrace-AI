# FinTrace AI

## AI-Powered Financial Reconciliation & Investigation Agent

FinTrace AI is a Python-based financial reconciliation and investigation application built with Streamlit. It analyzes invoices, payments, refunds, and accounting records to identify reconciliation issues, detect financial anomalies, and generate investigation insights.

---

## 🚀 Key Features

- 📄 Invoice data analysis
- 💳 Payment reconciliation
- ↩️ Refund tracking
- 📒 Accounting record comparison
- 🔍 Transaction reconciliation
- 🚨 Anomaly detection
- ⚠️ Severity classification
- 💰 Financial impact analysis
- 🕵️ Automated investigation report
- 📊 Financial overview dashboard
- 📁 CSV file upload
- 🔄 Automatic column mapping
- ✅ Data validation
- 📋 Transaction-level results
- 💡 Recommended actions for detected issues

---

## 🎯 Problem Statement

Financial organizations often maintain invoices, payments, refunds, and accounting records in separate datasets.

Manually comparing these records can be time-consuming and may lead to missed:

- Payment mismatches
- Unreconciled transactions
- Refund-related issues
- Accounting differences
- Financial anomalies

FinTrace AI automates this process by combining reconciliation, anomaly detection, and investigation into a single dashboard.

---

## 🏗️ System Workflow

```text
                    ┌─────────────────┐
                    │  Invoice CSV    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Payment CSV    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Refund CSV    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Accounting CSV  │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Automatic Data      │
                  │ Mapping & Validation│
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Transaction         │
                  │ Reconciliation      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Anomaly Detection   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Investigation       │
                  │ Report              │
                  └─────────────────────┘



                  ## 📥 Input Data

FinTrace AI accepts four financial CSV files.
### 1. Invoices
Typical fields:
- invoice_id
- amount
- vendor
- department
- date
### 2. Payments
Typical fields:
- payment_id
- invoice_id
- amount
- status
- date
### 3. Refunds
Typical fields:
- refund_id
- payment_id
- amount
- reason
- date
### 4. Accounting
Typical fields:
- entry_id
- invoice_id
- recorded_expense
- date
The application includes automatic column mapping to support common variations in uploaded column names.

## ⚙️ Installation
### Step 1 — Clone the repository
git clone https://github.com/syedmoin0800-byte/FinTrace-AI.git

### Step 2 — Open the project
cd FinTrace-AI

### Step 3 — Create a virtual environment

Windows:
python -m venv venv

### Step 4 — Activate the environment

Windows:
venv\Scripts\activate

### Step 5 — Install dependencies
pip install -r requirements.txt

## ▶️ Running the Application
Run:
python -m streamlit run app.py
Streamlit will start the FinTrace AI dashboard in your browser.

## 🧭 How to Use

### Step 1
Open the FinTrace AI application.
### Step 2

Upload the four required CSV files:
- Invoices
- Payments
- Refunds
- Accounting

### Step 3
Click:
🚀 Submit & Analyze

### Step 4
FinTrace AI performs the following processing stages:
1. Reading Financial Files
2. Mapping Data
3. Validating Data
4. Financial Reconciliation
5. Anomaly Investigation

### Step 5
Review the generated results.
## 🔍 Transaction Reconciliation
The Transaction Reconciliation section compares financial records and presents transaction-level information such as:
- Invoice ID
- Payment ID
- Invoice amount
- Payment amount
- Refund amount
- Recorded expense
- Expected expense
- Accounting difference
- Reconciliation status
- Issue type
- Anomaly type
- Severity
- Financial impact
This allows users to identify problematic transactions quickly.
## 🚨 Anomaly Detection
FinTrace AI analyzes reconciliation results to identify potential anomalies.
Detected issues can be classified by severity, including:
- LOW
- HIGH
- CRITICAL
Transactions without an identified anomaly are also displayed as:
- NO ANOMALY

## 🕵️ Investigation Report
For analyzed transactions, FinTrace AI generates an investigation section containing:
- Anomaly details
- Severity
- Financial impact
- Reason
- Financial evidence
- Investigation explanation
- Recommended action
This helps users understand not only what went wrong, but also the potential financial impact and suggested next action.

## 📊 Financial Dashboard
The dashboard provides an overview of:
- Total invoices
- Total payments
- Total refunds
- Total anomaly impact
- Reconciled transactions
- Unreconciled transactions
- Detected anomalies

## 🛡️ Data Validation
Before reconciliation, FinTrace AI validates the uploaded datasets.
The application checks whether required financial columns are available.
If required information is missing, the application displays a validation message instead of proceeding with an invalid reconciliation process.

## 🧪 Testing
The application was tested through a complete functional test cycle.

### Test Results
Test | Description | Result
--- | --- | ---
Test 1 | Empty State | ✅ PASS
Test 2 | Upload Validation | ✅ PASS
Test 3 | Complete Upload & Submit | ✅ PASS
Test 4 | Data Structure Detection | ✅ PASS
Test 5 | Financial Overview | ✅ PASS
Test 6 | Reconciliation Summary | ✅ PASS
Test 7 | Anomaly Analysis | ✅ PASS
Test 8 | Transaction Reconciliation | ✅ PASS
Test 9 | Investigation Report | ✅ PASS
Test 10 | File Change Detection | ✅ PASS


### Overall Result
10 / 10 TESTS PASSED ✅

## 🔄 File Change Detection
FinTrace AI was also tested with modified financial data.
When an uploaded financial file is changed and submitted again, the application processes the updated data instead of blindly displaying the previous analysis.
This verifies that the reconciliation results respond to changes in the input data.
## 💡 Example Use Cases
FinTrace AI can be useful for:
- Financial reconciliation
- Invoice verification
- Payment auditing
- Refund investigation
- Accounting comparison
- Transaction monitoring
- Financial anomaly identification
- Internal audit support


## 🔮 Future Enhancements
Possible future improvements include:
- Database integration
- Real-time financial data processing
- Advanced machine-learning anomaly detection
- User authentication
- Role-based access control
- Automated email alerts
- PDF investigation reports
- Excel export
- Advanced financial dashboards
- Cloud deployment
- Large-scale enterprise data processing


## 👨‍💻 Author
Syed Moin S
Electronics & Communication Engineering
AMC Engineering College
Bangalore, Karnataka, India


## 📜 License
This project is intended for educational, academic, and portfolio purposes.


## ⭐ Project Status
Status: Completed
Testing: 10/10 Passed
Core Reconciliation: Working
Anomaly Detection: Working
Investigation Report: Working
Transaction Reconciliation: Working


## 🙌 Acknowledgement
FinTrace AI was developed as a practical project to explore financial data processing, reconciliation, anomaly detection, and automated investigation using Python and Streamlit.

Note: This document contains the README.md content provided for the FinTrace AI project.
