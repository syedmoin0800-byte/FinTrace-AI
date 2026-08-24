import streamlit as st
import pandas as pd

from src.reconciliation import reconcile_financial_records
from src.investigation import generate_investigation


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
# KEY METRICS
# --------------------------------------------------

total_invoices = len(invoices)

total_payments = payments["amount"].sum()

total_refunds = refunds["amount"].sum()

total_accounting = accounting["recorded_expense"].sum()

total_mismatch = result["accounting_difference"].abs().sum()

unreconciled_count = (
    result["reconciliation_status"] == "UNRECONCILED"
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
        "Total Mismatch",
        f"₹{total_mismatch:,.0f}"
    )


# --------------------------------------------------
# RECONCILIATION SUMMARY
# --------------------------------------------------

st.markdown("---")

st.header("🔍 Reconciliation Summary")

col1, col2 = st.columns(2)

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


# --------------------------------------------------
# TRANSACTION RESULTS
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
    "issue_type"
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

    if row["reconciliation_status"] == "UNRECONCILED":

        with st.expander(
            f"⚠️ {row['invoice_id']} — "
            f"{row['issue_type']}"
        ):

            st.write("### Financial Evidence")

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
                f"**Financial Difference:** "
                f"₹{row['accounting_difference']:,.0f}"
            )

            st.markdown("### 📝 Explanation")

            st.info(explanation)

            st.markdown("### 💡 Recommended Action")

            st.warning(recommendation)

    else:

        with st.expander(
            f"✅ {row['invoice_id']} — Reconciled"
        ):

            st.success(explanation)

            st.write(
                f"**Recommended Action:** "
                f"{recommendation}"
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "FinTrace AI — Automated Financial Reconciliation & Investigation"
)