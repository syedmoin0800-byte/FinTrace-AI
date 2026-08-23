import streamlit as st

st.set_page_config(
    page_title="FinTrace AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinTrace AI")
st.subheader("AI-Powered Financial Reconciliation & Investigation Agent")

st.markdown("---")

st.header("Problem Statement")

st.write("""
Businesses often struggle to reconcile payments, refunds, settlements, and accounting records.
When these records don't match, identifying the cause and financial impact becomes a slow manual process.
FinTrace AI automatically detects, investigates, and explains these financial mismatches.
""")

st.success("✅ FinTrace AI Project Initialized Successfully")