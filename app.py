import streamlit as st
import pandas as pd

from src.reconciliation import reconcile_financial_records
from src.investigation import generate_investigation
from src.anomaly_analyzer import analyze_anomaly


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FinTrace AI",
    page_icon="💰",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    invoices = pd.read_csv("data/invoices.csv")
    payments = pd.read_csv("data/payments.csv")
    refunds = pd.read_csv("data/refunds.csv")
    accounting = pd.read_csv("data/accounting.csv")

    return invoices, payments, refunds, accounting


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("💰 FinTrace AI")

st.subheader(
    "AI-Powered Financial Reconciliation & Investigation Agent"
)

st.markdown("---")


# --------------------------------------------------
# LOAD AND RECONCILE
# --------------------------------------------------

invoices, payments, refunds, accounting = load_data()

result = reconcile_financial_records(
    invoices,
    payments,
    refunds,
    accounting
)


# --------------------------------------------------
# ANOMALY ANALYSIS
# --------------------------------------------------

anomaly_results = []

for _, row in result.iterrows():

    analysis = analyze_anomaly(row)

    anomaly_results.append(analysis)


anomaly_df = pd.DataFrame(anomaly_results)

result = pd.concat(
    [
        result.reset_index(drop=True),
        anomaly_df.reset_index(drop=True)
    ],
    axis=1
)


# --------------------------------------------------
# KEY METRICS
# --------------------------------------------------

total_invoices = len(invoices)

total_payments = payments["amount"].sum()

total_refunds = refunds["amount"].sum()

total_mismatch = result["financial_impact"].sum()

unreconciled_count = (
    result["reconciliation_status"] == "UNRECONCILED"
).sum()

anomaly_count = (
    result["anomaly_type"] != "NO ANOMALY"
).sum()


st.header("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Invoices",
        total_invoices
    )

with col2:
    st.metric(
        "Total Payments",
        f"₹{total_payments:,.0f}"
    )

with col3:
    st.metric(
        "Total Refunds",
        f"₹{total_refunds:,.0f}"
    )

with col4:
    st.metric(
        "Total Anomaly Impact",
        f"₹{total_mismatch:,.0f}"
    )


# --------------------------------------------------
# RECONCILIATION SUMMARY
# --------------------------------------------------

st.markdown("---")

st.header("🔍 Reconciliation Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        f"✅ Reconciled Transactions: "
        f"{len(result) - unreconciled_count}"
    )

with col2:
    st.error(
        f"⚠️ Unreconciled Transactions: "
        f"{unreconciled_count}"
    )

with col3:
    st.warning(
        f"🚨 Anomalies Detected: "
        f"{anomaly_count}"
    )


# --------------------------------------------------
# ANOMALY SUMMARY
# --------------------------------------------------

st.markdown("---")

st.header("🚨 Anomaly Analysis")

for _, row in result.iterrows():

    if row["anomaly_type"] == "NO ANOMALY":

        st.success(
            f"✅ {row['invoice_id']} — No anomaly detected"
        )

    else:

        if row["severity"] == "CRITICAL":
            st.error(
                f"🔴 {row['invoice_id']} — "
                f"{row['anomaly_type']} — "
                f"CRITICAL"
            )

        elif row["severity"] == "HIGH":
            st.warning(
                f"🟠 {row['invoice_id']} — "
                f"{row['anomaly_type']} — "
                f"HIGH"
            )

        else:
            st.info(
                f"🟡 {row['invoice_id']} — "
                f"{row['anomaly_type']} — "
                f"{row['severity']}"
            )


# --------------------------------------------------
# TRANSACTION RECONCILIATION
# --------------------------------------------------

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
    "financial_impact"
]

st.dataframe(
    result[display_columns],
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# INVESTIGATION REPORT
# --------------------------------------------------

st.markdown("---")

st.header("🕵️ Investigation Report")

for _, row in result.iterrows():

    explanation, recommendation = generate_investigation(row)

    with st.expander(
        f"{'⚠️' if row['anomaly_type'] != 'NO ANOMALY' else '✅'} "
        f"{row['invoice_id']} — {row['anomaly_type']}"
    ):

        st.markdown("### 🚨 Anomaly Details")

        st.write(
            f"**Anomaly Type:** "
            f"{row['anomaly_type']}"
        )

        st.write(
            f"**Severity:** "
            f"{row['severity']}"
        )

        st.write(
            f"**Financial Impact:** "
            f"₹{row['financial_impact']:,.0f}"
        )

        st.write(
            f"**Reason:** "
            f"{row['reason']}"
        )

        st.markdown("### 💰 Financial Evidence")

        st.write(
            f"**Invoice Amount:** "
            f"₹{row['amount_invoice']:,.0f}"
        )

        st.write(
            f"**Payment Amount:** "
            f"₹{row['amount_payment']:,.0f}"
        )

        st.write(
            f"**Refund Amount:** "
            f"₹{row['refund_amount']:,.0f}"
        )

        st.write(
            f"**Accounting Expense:** "
            f"₹{row['recorded_expense']:,.0f}"
        )

        st.write(
            f"**Expected Expense:** "
            f"₹{row['expected_expense']:,.0f}"
        )

        st.write(
            f"**Accounting Difference:** "
            f"₹{row['accounting_difference']:,.0f}"
        )

        st.markdown("### 📝 Investigation Explanation")

        st.info(explanation)

        st.markdown("### 💡 Recommended Action")

        if row["anomaly_type"] == "NO ANOMALY":
            st.success(recommendation)
        else:
            st.warning(recommendation)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "FinTrace AI — Automated Financial Reconciliation, "
    "Anomaly Detection & Investigation"
)
