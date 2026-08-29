import streamlit as st
import pandas as pd
import time
 
from src.data_mapper import map_columns
from src.reconciliation import reconcile_financial_records
from src.investigation import generate_investigation
from src.anomaly_analyzer import analyze_anomaly
 
st.set_page_config(page_title="FinTrace AI", page_icon="💰", layout="wide")
 
if "files_submitted" not in st.session_state:
    st.session_state["files_submitted"] = False
if "submitted_signature" not in st.session_state:
    st.session_state["submitted_signature"] = None
 
 
def file_signature(files):
    if not all(files):
        return None
    return tuple(
        item for file in files for item in (file.name, file.size)
    )
 
 
def empty_financial_data():
    return (
        pd.DataFrame(columns=["invoice_id", "vendor", "department", "amount", "date"]),
        pd.DataFrame(columns=["payment_id", "invoice_id", "amount", "status", "date"]),
        pd.DataFrame(columns=["refund_id", "payment_id", "amount", "reason", "date"]),
        pd.DataFrame(columns=["entry_id", "invoice_id", "recorded_expense", "date"]),
    )
 
 
def check_required_columns(invoices, payments, refunds, accounting):
    required = {
        "Invoices": ["invoice_id", "amount"],
        "Payments": ["payment_id", "invoice_id", "amount"],
        "Refunds": ["refund_id", "payment_id", "amount"],
        "Accounting": ["entry_id", "invoice_id", "recorded_expense"],
    }
    datasets = {
        "Invoices": invoices,
        "Payments": payments,
        "Refunds": refunds,
        "Accounting": accounting,
    }
    errors = []
    for name, columns in required.items():
        missing = [col for col in columns if col not in datasets[name].columns]
        if missing:
            errors.append(f"{name}: missing {', '.join(missing)}")
    return errors
 
 
def show_processing_step(placeholder, progress_bar, number, title, description, value, delay=0.6):
    placeholder.markdown(
        f"""
        <div style="text-align:center;padding:30px;font-size:24px;">
            🔄 <b>Step {number} of 5 — {title}</b><br><br>
            <span style="font-size:16px;">{description}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    progress_bar.progress(value)
    time.sleep(delay)
 
 
def convert_numeric(invoices, payments, refunds, accounting):
    invoices["amount"] = pd.to_numeric(invoices["amount"], errors="coerce")
    payments["amount"] = pd.to_numeric(payments["amount"], errors="coerce")
    refunds["amount"] = pd.to_numeric(refunds["amount"], errors="coerce")
    accounting["recorded_expense"] = pd.to_numeric(
        accounting["recorded_expense"], errors="coerce"
    )
    return invoices, payments, refunds, accounting
 
 
def analyze_anomalies(result):
    columns = ["anomaly_type", "severity", "financial_impact"]
    if result.empty:
        return pd.DataFrame(columns=columns)
 
    analyses = []
    for _, row in result.iterrows():
        try:
            value = analyze_anomaly(row)
            analyses.append(value if isinstance(value, dict) else {})
        except Exception:
            analyses.append({})
 
    anomaly_df = pd.DataFrame(analyses)
    for column in columns:
        if column not in anomaly_df.columns:
            anomaly_df[column] = None
    return anomaly_df[columns]
 
 
st.title("💰 FinTrace AI")
st.subheader("AI-Powered Financial Reconciliation & Investigation Agent")
st.markdown("---")
 
st.sidebar.header("📂 Financial Data")
st.sidebar.write(
    "Upload your financial CSV files. "
    "FinTrace AI will automatically map common column names."
)
 
invoice_file = st.sidebar.file_uploader(
    "📄 Upload Invoices CSV", type=["csv"], key="invoices"
)
payment_file = st.sidebar.file_uploader(
    "💳 Upload Payments CSV", type=["csv"], key="payments"
)
refund_file = st.sidebar.file_uploader(
    "↩️ Upload Refunds CSV", type=["csv"], key="refunds"
)
accounting_file = st.sidebar.file_uploader(
    "📒 Upload Accounting CSV", type=["csv"], key="accounting"
)
 
files = [invoice_file, payment_file, refund_file, accounting_file]
all_files_uploaded = all(file is not None for file in files)
current_signature = file_signature(files)
 
if (
    st.session_state["submitted_signature"] is not None
    and current_signature != st.session_state["submitted_signature"]
):
    st.session_state["files_submitted"] = False
    st.session_state["submitted_signature"] = None
 
st.sidebar.markdown("---")
 
if all_files_uploaded:
    st.sidebar.success("✅ All 4 files are ready.")
    if st.sidebar.button("🚀 Submit & Analyze", use_container_width=True):
        st.session_state["files_submitted"] = True
        st.session_state["submitted_signature"] = current_signature
else:
    st.session_state["files_submitted"] = False
    st.session_state["submitted_signature"] = None
    st.sidebar.info("📌 Upload all 4 CSV files to continue.")
 
 
if not st.session_state["files_submitted"]:
    invoices, payments, refunds, accounting = empty_financial_data()
 
    st.info(
        "📁 Upload all four financial CSV files from the sidebar, "
        "then click 🚀 Submit & Analyze to start analysis."
    )
 
    st.header("📊 Financial Overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Invoices", 0)
    with c2:
        st.metric("Total Payments", "₹0")
    with c3:
        st.metric("Total Refunds", "₹0")
    with c4:
        st.metric("Total Anomaly Impact", "₹0")
 
    st.markdown("---")
    st.header("🔍 Reconciliation Summary")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.success("✅ Reconciled Transactions: 0")
    with c2:
        st.error("⚠️ Unreconciled Transactions: 0")
    with c3:
        st.warning("🚨 Anomalies Detected: 0")
 
    st.markdown("---")
    st.info("💡 Results will appear here after your files are submitted and analyzed.")
    st.stop()
 
 
processing_box = st.empty()
progress_bar = st.progress(0)
 
show_processing_step(
    processing_box, progress_bar, 1, "Reading Financial Files",
    "Loading invoices, payments, refunds and accounting data...", 20
)
 
try:
    invoices = pd.read_csv(invoice_file)
    payments = pd.read_csv(payment_file)
    refunds = pd.read_csv(refund_file)
    accounting = pd.read_csv(accounting_file)
except Exception as e:
    processing_box.empty()
    progress_bar.empty()
    st.error(f"❌ Unable to read uploaded CSV files: {e}")
    st.stop()
 
 
show_processing_step(
    processing_box, progress_bar, 2, "Mapping Data",
    "Detecting and mapping financial column names...", 40
)
 
try:
    invoices = map_columns(invoices)
    payments = map_columns(payments)
    refunds = map_columns(refunds)
    accounting = map_columns(accounting)
except Exception as e:
    processing_box.empty()
    progress_bar.empty()
    st.error(f"❌ Data mapping failed: {e}")
    st.stop()
 
 
show_processing_step(
    processing_box, progress_bar, 3, "Validating Data",
    "Checking required columns and financial values...", 60
)
 
errors = check_required_columns(invoices, payments, refunds, accounting)
if errors:
    processing_box.empty()
    progress_bar.empty()
    st.error("❌ Data structure validation failed.")
    for error in errors:
        st.warning(error)
    st.info("Please upload CSV files containing the required financial information.")
    st.stop()
 
try:
    invoices, payments, refunds, accounting = convert_numeric(
        invoices, payments, refunds, accounting
    )
except Exception as e:
    processing_box.empty()
    progress_bar.empty()
    st.error(f"❌ Numeric conversion failed: {e}")
    st.stop()
 
datasets = {
    "Invoices": invoices,
    "Payments": payments,
    "Refunds": refunds,
    "Accounting": accounting,
}
invalid_data = any(df.isnull().any().any() for df in datasets.values())
 
 
show_processing_step(
    processing_box, progress_bar, 4, "Financial Reconciliation",
    "Matching invoices, payments, refunds and accounting records...", 80
)
 
try:
    result = reconcile_financial_records(
        invoices, payments, refunds, accounting
    )
except Exception as e:
    processing_box.empty()
    progress_bar.empty()
    st.error(f"❌ Reconciliation failed: {e}")
    st.stop()
 
 
show_processing_step(
    processing_box, progress_bar, 5, "Anomaly Investigation",
    "Detecting anomalies and evaluating financial impact...", 100, 0.8
)
 
anomaly_df = analyze_anomalies(result)
result = pd.concat(
    [result.reset_index(drop=True), anomaly_df.reset_index(drop=True)],
    axis=1,
)
 
time.sleep(0.3)
progress_bar.empty()
processing_box.empty()
 
st.success("📂 Financial files analyzed successfully.")
if invalid_data:
    st.warning(
        "⚠️ Some uploaded files contain missing values. Results may be affected."
    )
 
 
with st.expander("🔎 View Detected Data Structure"):
    tabs = st.tabs(["Invoices", "Payments", "Refunds", "Accounting"])
    datasets = {
        "Invoices": invoices,
        "Payments": payments,
        "Refunds": refunds,
        "Accounting": accounting,
    }
    for tab, (name, df) in zip(tabs, datasets.items()):
        with tab:
            st.write("**Detected columns:**")
            st.write(list(df.columns))
            st.dataframe(df.head(), width="stretch", hide_index=True)
 
 
total_invoices = len(invoices)
total_payments = pd.to_numeric(
    payments["amount"], errors="coerce"
).fillna(0).sum()
total_refunds = pd.to_numeric(
    refunds["amount"], errors="coerce"
).fillna(0).sum()
 
if "financial_impact" in result.columns:
    total_mismatch = pd.to_numeric(
        result["financial_impact"], errors="coerce"
    ).fillna(0).sum()
else:
    total_mismatch = 0
 
if "reconciliation_status" in result.columns:
    unreconciled_count = (
        result["reconciliation_status"] == "UNRECONCILED"
    ).sum()
else:
    unreconciled_count = 0
 
if "anomaly_type" in result.columns:
    anomaly_count = (
        result["anomaly_type"] != "NO ANOMALY"
    ).sum()
else:
    anomaly_count = 0
 
 
st.header("📊 Financial Overview")
c1, c2, c3, c4 = st.columns(4)
 
with c1:
    st.metric("Total Invoices", total_invoices)
with c2:
    st.metric("Total Payments", f"₹{total_payments:,.0f}")
with c3:
    st.metric("Total Refunds", f"₹{total_refunds:,.0f}")
with c4:
    st.metric("Total Anomaly Impact", f"₹{total_mismatch:,.0f}")
 
 
st.markdown("---")
st.header("🔍 Reconciliation Summary")
c1, c2, c3 = st.columns(3)
 
with c1:
    st.success(f"✅ Reconciled Transactions: {len(result) - unreconciled_count}")
with c2:
    st.error(f"⚠️ Unreconciled Transactions: {unreconciled_count}")
with c3:
    st.warning(f"🚨 Anomalies Detected: {anomaly_count}")
 
 
st.markdown("---")
st.header("🚨 Anomaly Analysis")
 
if result.empty:
    st.info("No transactions available for analysis.")
else:
    for _, row in result.iterrows():
        anomaly_type = row.get("anomaly_type", "NO ANOMALY")
        severity = row.get("severity", "LOW")
        invoice_id = row.get("invoice_id", "UNKNOWN")
 
        if anomaly_type == "NO ANOMALY":
            st.success(f"✅ {invoice_id} — No anomaly detected")
        elif severity == "CRITICAL":
            st.error(f"🔴 {invoice_id} — {anomaly_type} — CRITICAL")
        elif severity == "HIGH":
            st.warning(f"🟠 {invoice_id} — {anomaly_type} — HIGH")
        else:
            st.info(f"🟡 {invoice_id} — {anomaly_type} — {severity}")
 
 
st.markdown("---")
st.header("📋 Transaction Reconciliation")
 
display_columns = [
    "invoice_id",
    "payment_id",
    "amount_invoice",
    "amount_payment",
    "refund_amount",
    "recorded_expense",
    "expected_expense",
    "accounting_difference",
    "reconciliation_status",
    "issue_type",
    "anomaly_type",
    "severity",
    "financial_impact",
]
 
available_columns = [
    column for column in display_columns if column in result.columns
]
 
if available_columns:
    st.dataframe(
        result[available_columns],
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No reconciliation columns are available.")
 
 
st.markdown("---")
st.header("🕵️ Investigation Report")
 
if result.empty:
    st.info("No transactions available for investigation.")
else:
    for _, row in result.iterrows():
        anomaly_type = row.get("anomaly_type", "NO ANOMALY")
        invoice_id = row.get("invoice_id", "UNKNOWN")
        explanation, recommendation = generate_investigation(row)
 
        icon = "⚠️" if anomaly_type != "NO ANOMALY" else "✅"
 
        with st.expander(f"{icon} {invoice_id} — {anomaly_type}"):
            st.markdown("### 🚨 Anomaly Details")
            st.write(f"**Anomaly Type:** {anomaly_type}")
            st.write(f"**Severity:** {row.get('severity', 'LOW')}")
 
            impact = pd.to_numeric(
                row.get("financial_impact", 0), errors="coerce"
            )
            if pd.isna(impact):
                impact = 0
            st.write(f"**Financial Impact:** ₹{impact:,.0f}")
            st.write(f"**Reason:** {row.get('reason', 'Not available')}")
 
            st.markdown("### 💰 Financial Evidence")
 
            evidence = [
                ("Invoice Amount", "amount_invoice"),
                ("Payment Amount", "amount_payment"),
                ("Refund Amount", "refund_amount"),
                ("Accounting Expense", "recorded_expense"),
                ("Expected Expense", "expected_expense"),
                ("Accounting Difference", "accounting_difference"),
            ]
 
            for label, field in evidence:
                value = pd.to_numeric(
                    row.get(field, 0), errors="coerce"
                )
                if pd.isna(value):
                    value = 0
                st.write(f"**{label}:** ₹{value:,.0f}")
 
            st.markdown("### 📝 Investigation Explanation")
            st.info(explanation)
 
            st.markdown("### 💡 Recommended Action")
            if anomaly_type == "NO ANOMALY":
                st.success(recommendation)
            else:
                st.warning(recommendation)
 
 
st.markdown("---")
st.caption(
    "FinTrace AI — Automated Financial Reconciliation, "
    "Anomaly Detection & Investigation"
)
