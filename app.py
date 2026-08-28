import streamlit as st
import pandas as pd
import time
import hashlib

from src.data_mapper import map_columns
from src.reconciliation import reconcile_financial_records
from src.investigation import generate_investigation
from src.anomaly_analyzer import analyze_anomaly


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinTrace AI",
    page_icon="💰",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "files_submitted" not in st.session_state:
    st.session_state["files_submitted"] = False

if "submitted_signature" not in st.session_state:
    st.session_state["submitted_signature"] = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_file_signature(uploaded_file):
    """Create a stable signature for an uploaded file."""

    if uploaded_file is None:
        return None

    return hashlib.md5(
        uploaded_file.getvalue()
    ).hexdigest()


def safe_number(value):
    """Safely convert a value to float."""

    try:
        if pd.isna(value):
            return 0.0

        return float(value)

    except (TypeError, ValueError):
        return 0.0


def safe_text(value, default="N/A"):
    """Safely convert a value to display text."""

    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass

    return str(value)


def show_processing_step(
    box,
    progress,
    step_number,
    title,
    description,
    percentage
):
    """Display a consistent processing step."""

    box.markdown(
        f"""
        <div style="
            text-align:center;
            padding:30px;
            font-size:24px;
        ">
            <div>
                <b>{title}</b>
            </div>

            <br>

            <span style="font-size:16px;">
                {description}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    progress.progress(percentage)

    time.sleep(0.7)


def check_required_columns(
    invoices,
    payments,
    refunds,
    accounting
):
    """Check whether all required FinTrace columns exist."""

    required_columns = {
        "Invoices": [
            "invoice_id",
            "amount"
        ],

        "Payments": [
            "payment_id",
            "invoice_id",
            "amount"
        ],

        "Refunds": [
            "refund_id",
            "payment_id",
            "amount"
        ],

        "Accounting": [
            "entry_id",
            "invoice_id",
            "recorded_expense"
        ]
    }

    datasets = {
        "Invoices": invoices,
        "Payments": payments,
        "Refunds": refunds,
        "Accounting": accounting
    }

    errors = []

    for name, required in required_columns.items():

        missing = [
            column
            for column in required
            if column not in datasets[name].columns
        ]

        if missing:

            errors.append(
                f"{name}: missing {', '.join(missing)}"
            )

    return errors


# ============================================================
# HEADER
# ============================================================

st.title("💰 FinTrace AI")

st.subheader(
    "AI-Powered Financial Reconciliation & Investigation Agent"
)

st.markdown("---")


# ============================================================
# SIDEBAR - FILE INPUT
# ============================================================

st.sidebar.header("📂 Financial Data")

st.sidebar.write(
    "Upload all four financial CSV files. "
    "FinTrace AI will map common column names automatically."
)


invoice_file = st.sidebar.file_uploader(
    "📄 Upload Invoices CSV",
    type=["csv"],
    key="invoices"
)


payment_file = st.sidebar.file_uploader(
    "💳 Upload Payments CSV",
    type=["csv"],
    key="payments"
)


refund_file = st.sidebar.file_uploader(
    "↩️ Upload Refunds CSV",
    type=["csv"],
    key="refunds"
)


accounting_file = st.sidebar.file_uploader(
    "📒 Upload Accounting CSV",
    type=["csv"],
    key="accounting"
)


# ============================================================
# FILE STATUS
# ============================================================

all_files_uploaded = all([
    invoice_file is not None,
    payment_file is not None,
    refund_file is not None,
    accounting_file is not None
])


# ============================================================
# FILE SIGNATURE
# ============================================================

current_signature = None

if all_files_uploaded:

    current_signature = (
        get_file_signature(invoice_file),
        get_file_signature(payment_file),
        get_file_signature(refund_file),
        get_file_signature(accounting_file)
    )


# ============================================================
# RESET WHEN FILES CHANGE
# ============================================================

if (
    st.session_state["submitted_signature"] is not None
    and current_signature !=
        st.session_state["submitted_signature"]
):

    st.session_state["files_submitted"] = False

    st.session_state["submitted_signature"] = None


# ============================================================
# SUBMIT BUTTON
# ============================================================

st.sidebar.markdown("---")


if all_files_uploaded:

    st.sidebar.success(
        "✅ All 4 files are ready."
    )

    if st.sidebar.button(
        "🚀 Submit & Analyze",
        width="stretch"
    ):

        st.session_state["files_submitted"] = True

        st.session_state["submitted_signature"] = (
            current_signature
        )

else:

    st.session_state["files_submitted"] = False

    st.session_state["submitted_signature"] = None

    st.sidebar.info(
        "📌 Upload all 4 CSV files to continue."
    )


# ============================================================
# INITIAL EMPTY DASHBOARD
# ============================================================

if not st.session_state["files_submitted"]:

    st.info(
        "📁 Upload all four financial CSV files from the sidebar, "
        "then click 🚀 Submit & Analyze to start analysis."
    )


    # --------------------------------------------------------
    # FINANCIAL OVERVIEW
    # --------------------------------------------------------

    st.header("📊 Financial Overview")

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total Invoices",
            0
        )


    with col2:

        st.metric(
            "Total Payments",
            "₹0"
        )


    with col3:

        st.metric(
            "Total Refunds",
            "₹0"
        )


    with col4:

        st.metric(
            "Total Anomaly Impact",
            "₹0"
        )


    # --------------------------------------------------------
    # RECONCILIATION SUMMARY
    # --------------------------------------------------------

    st.markdown("---")

    st.header("🔍 Reconciliation Summary")

    col1, col2, col3 = st.columns(3)


    with col1:

        st.success(
            "✅ Reconciled Transactions: 0"
        )


    with col2:

        st.error(
            "⚠️ Unreconciled Transactions: 0"
        )


    with col3:

        st.warning(
            "🚨 Anomalies Detected: 0"
        )


    st.markdown("---")

    st.info(
        "💡 Results will appear here after your files "
        "are submitted and analyzed."
    )


    # IMPORTANT:
    # No processing occurs before Submit.

    st.stop()


# ============================================================
# PROCESSING UI
# ============================================================

processing_box = st.empty()

progress_bar = st.progress(0)


# ============================================================
# STEP 1 - READ FILES
# ============================================================

show_processing_step(
    processing_box,
    progress_bar,
    1,
    "📥 Step 1 of 5 — Reading Financial Files",
    "Loading invoices, payments, refunds and accounting data...",
    20
)


try:

    invoices = pd.read_csv(invoice_file)

    payments = pd.read_csv(payment_file)

    refunds = pd.read_csv(refund_file)

    accounting = pd.read_csv(accounting_file)


except Exception as e:

    processing_box.empty()

    progress_bar.empty()

    st.error(
        f"❌ Unable to read uploaded CSV files: {e}"
    )

    st.session_state["files_submitted"] = False

    st.stop()


# ============================================================
# STEP 2 - DATA MAPPING
# ============================================================

show_processing_step(
    processing_box,
    progress_bar,
    2,
    "🔄 Step 2 of 5 — Mapping Data",
    "Detecting and mapping financial column names...",
    40
)


try:

    invoices = map_columns(invoices)

    payments = map_columns(payments)

    refunds = map_columns(refunds)

    accounting = map_columns(accounting)


except Exception as e:

    processing_box.empty()

    progress_bar.empty()

    st.error(
        f"❌ Data mapping failed: {e}"
    )

    st.session_state["files_submitted"] = False

    st.stop()


# ============================================================
# STEP 3 - VALIDATION
# ============================================================

show_processing_step(
    processing_box,
    progress_bar,
    3,
    "🔎 Step 3 of 5 — Validating Data",
    "Checking required columns and financial values...",
    60
)


errors = check_required_columns(
    invoices,
    payments,
    refunds,
    accounting
)


if errors:

    processing_box.empty()

    progress_bar.empty()

    st.error(
        "❌ Data structure validation failed."
    )

    for error in errors:

        st.warning(
            f"⚠️ {error}"
        )

    st.info(
        "Please upload four compatible financial CSV files."
    )

    st.session_state["files_submitted"] = False

    st.stop()


# ============================================================
# NUMERIC CONVERSION
# ============================================================

try:

    invoices["amount"] = pd.to_numeric(
        invoices["amount"],
        errors="coerce"
    )

    payments["amount"] = pd.to_numeric(
        payments["amount"],
        errors="coerce"
    )

    refunds["amount"] = pd.to_numeric(
        refunds["amount"],
        errors="coerce"
    )

    accounting["recorded_expense"] = pd.to_numeric(
        accounting["recorded_expense"],
        errors="coerce"
    )


except Exception as e:

    processing_box.empty()

    progress_bar.empty()

    st.error(
        f"❌ Numeric conversion failed: {e}"
    )

    st.session_state["files_submitted"] = False

    st.stop()


# ============================================================
# DATA QUALITY CHECK
# ============================================================

invalid_data = False

missing_summary = {}

datasets = {
    "Invoices": invoices,
    "Payments": payments,
    "Refunds": refunds,
    "Accounting": accounting
}


for name, df in datasets.items():

    missing_count = int(
        df.isnull().sum().sum()
    )

    missing_summary[name] = missing_count

    if missing_count > 0:

        invalid_data = True


# ============================================================
# STEP 4 - RECONCILIATION
# ============================================================

show_processing_step(
    processing_box,
    progress_bar,
    4,
    "🔍 Step 4 of 5 — Financial Reconciliation",
    "Matching invoices, payments, refunds and accounting records...",
    80
)


try:

    result = reconcile_financial_records(
        invoices,
        payments,
        refunds,
        accounting
    )


except Exception as e:

    processing_box.empty()

    progress_bar.empty()

    st.error(
        f"❌ Reconciliation failed: {e}"
    )

    st.session_state["files_submitted"] = False

    st.stop()


# ============================================================
# STEP 5 - ANOMALY ANALYSIS
# ============================================================

show_processing_step(
    processing_box,
    progress_bar,
    5,
    "🚨 Step 5 of 5 — Anomaly Investigation",
    "Detecting anomalies and evaluating financial impact...",
    100
)


# ============================================================
# ANOMALY ANALYSIS
# ============================================================

anomaly_columns = [
    "anomaly_type",
    "severity",
    "financial_impact"
]


if result.empty:

    anomaly_df = pd.DataFrame(
        columns=anomaly_columns
    )


else:

    anomaly_results = []


    for _, row in result.iterrows():

        try:

            analysis = analyze_anomaly(row)

            if isinstance(analysis, dict):

                anomaly_results.append(
                    analysis
                )

            else:

                anomaly_results.append({})


        except Exception:

            anomaly_results.append({})


    anomaly_df = pd.DataFrame(
        anomaly_results
    )


    # Ensure anomaly columns always exist.

    for column in anomaly_columns:

        if column not in anomaly_df.columns:

            anomaly_df[column] = None


    anomaly_df = anomaly_df[
        anomaly_columns
    ]


# ============================================================
# MERGE RESULTS
# ============================================================

result = pd.concat(
    [
        result.reset_index(drop=True),
        anomaly_df.reset_index(drop=True)
    ],
    axis=1
)


# ============================================================
# CLEAN PROCESSING UI
# ============================================================

time.sleep(0.5)

progress_bar.empty()

processing_box.empty()


# ============================================================
# SUCCESS MESSAGE
# ============================================================

st.success(
    "📂 Financial files analyzed successfully."
)


if invalid_data:

    missing_text = ", ".join(
        [
            f"{name}: {count}"
            for name, count
            in missing_summary.items()
            if count > 0
        ]
    )

    st.warning(
        "⚠️ Missing values detected — "
        + missing_text
    )


# ============================================================
# DATASET PREVIEW
# ============================================================

with st.expander(
    "🔎 View Detected Data Structure"
):

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Invoices",
            "Payments",
            "Refunds",
            "Accounting"
        ]
    )


    with tab1:

        st.write(
            "**Detected columns:**"
        )

        st.write(
            list(invoices.columns)
        )

        st.dataframe(
            invoices.head(),
            width="stretch",
            hide_index=True
        )


    with tab2:

        st.write(
            "**Detected columns:**"
        )

        st.write(
            list(payments.columns)
        )

        st.dataframe(
            payments.head(),
            width="stretch",
            hide_index=True
        )


    with tab3:

        st.write(
            "**Detected columns:**"
        )

        st.write(
            list(refunds.columns)
        )

        st.dataframe(
            refunds.head(),
            width="stretch",
            hide_index=True
        )


    with tab4:

        st.write(
            "**Detected columns:**"
        )

        st.write(
            list(accounting.columns)
        )

        st.dataframe(
            accounting.head(),
            width="stretch",
            hide_index=True
        )


# ============================================================
# FINANCIAL METRICS
# ============================================================

total_invoices = len(invoices)


total_payments = pd.to_numeric(
    payments["amount"],
    errors="coerce"
).fillna(0).sum()


total_refunds = pd.to_numeric(
    refunds["amount"],
    errors="coerce"
).fillna(0).sum()


total_mismatch = 0

if "financial_impact" in result.columns:

    total_mismatch = pd.to_numeric(
        result["financial_impact"],
        errors="coerce"
    ).fillna(0).sum()


unreconciled_count = 0

if "reconciliation_status" in result.columns:

    unreconciled_count = (
        result["reconciliation_status"]
        .astype(str)
        .str.upper()
        .eq("UNRECONCILED")
        .sum()
    )


anomaly_count = 0

if "anomaly_type" in result.columns:

    anomaly_count = (
        result["anomaly_type"]
        .fillna("NO ANOMALY")
        .astype(str)
        .str.upper()
        .ne("NO ANOMALY")
        .sum()
    )


reconciled_count = max(
    len(result) - unreconciled_count,
    0
)


# ============================================================
# FINANCIAL OVERVIEW
# ============================================================

st.header(
    "📊 Financial Overview"
)


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


# ============================================================
# RECONCILIATION SUMMARY
# ============================================================

st.markdown("---")

st.header(
    "🔍 Reconciliation Summary"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.success(
        f"✅ Reconciled Transactions: "
        f"{reconciled_count}"
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


# ============================================================
# ANOMALY ANALYSIS
# ============================================================

st.markdown("---")

st.header(
    "🚨 Anomaly Analysis"
)


if result.empty:

    st.info(
        "No transactions available for analysis."
    )


else:

    for _, row in result.iterrows():

        anomaly_type = safe_text(
            row.get(
                "anomaly_type",
                "NO ANOMALY"
            ),
            "NO ANOMALY"
        )

        severity = safe_text(
            row.get(
                "severity",
                "LOW"
            ),
            "LOW"
        )

        invoice_id = safe_text(
            row.get(
                "invoice_id",
                "UNKNOWN"
            ),
            "UNKNOWN"
        )


        if anomaly_type.upper() == "NO ANOMALY":

            st.success(
                f"✅ {invoice_id} — "
                f"No anomaly detected"
            )


        elif severity.upper() == "CRITICAL":

            st.error(
                f"🔴 {invoice_id} — "
                f"{anomaly_type} — CRITICAL"
            )


        elif severity.upper() == "HIGH":

            st.warning(
                f"🟠 {invoice_id} — "
                f"{anomaly_type} — HIGH"
            )


        else:

            st.info(
                f"🟡 {invoice_id} — "
                f"{anomaly_type} — {severity}"
            )


# ============================================================
# TRANSACTION RECONCILIATION
# ============================================================

st.markdown("---")

st.header(
    "📋 Transaction Reconciliation"
)


if result.empty:

    st.info(
        "No reconciliation records available."
    )


else:

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


    available_display_columns = [

        column

        for column in display_columns

        if column in result.columns

    ]


    if available_display_columns:

        st.dataframe(
            result[
                available_display_columns
            ],
            width="stretch",
            hide_index=True
        )


    else:

        st.warning(
            "⚠️ Reconciliation data was generated, "
            "but no standard display columns were found."
        )

        st.dataframe(
            result,
            width="stretch",
            hide_index=True
        )


# ============================================================
# INVESTIGATION REPORT
# ============================================================

st.markdown("---")

st.header(
    "🕵️ Investigation Report"
)


if result.empty:

    st.info(
        "No investigation records available."
    )


else:

    for _, row in result.iterrows():

        anomaly_type = safe_text(
            row.get(
                "anomaly_type",
                "NO ANOMALY"
            ),
            "NO ANOMALY"
        )

        invoice_id = safe_text(
            row.get(
                "invoice_id",
                "UNKNOWN"
            ),
            "UNKNOWN"
        )

        severity = safe_text(
            row.get(
                "severity",
                "LOW"
            ),
            "LOW"
        )


        try:

            explanation, recommendation = (
                generate_investigation(row)
            )


        except Exception:

            explanation = (
                "Investigation explanation "
                "could not be generated."
            )

            recommendation = (
                "Review the transaction manually."
            )


        icon = (
            "⚠️"
            if anomaly_type.upper()
            != "NO ANOMALY"
            else "✅"
        )


        with st.expander(
            f"{icon} {invoice_id} — "
            f"{anomaly_type}"
        ):


            # ------------------------------------------------
            # ANOMALY DETAILS
            # ------------------------------------------------

            st.markdown(
                "### 🚨 Anomaly Details"
            )


            st.write(
                f"**Anomaly Type:** "
                f"{anomaly_type}"
            )


            st.write(
                f"**Severity:** "
                f"{severity}"
            )


            financial_impact = safe_number(
                row.get(
                    "financial_impact",
                    0
                )
            )


            st.write(
                f"**Financial Impact:** "
                f"₹{financial_impact:,.0f}"
            )


            reason = safe_text(
                row.get(
                    "reason",
                    "No additional reason available."
                ),
                "No additional reason available."
            )


            st.write(
                f"**Reason:** {reason}"
            )


            # ------------------------------------------------
            # FINANCIAL EVIDENCE
            # ------------------------------------------------

            st.markdown(
                "### 💰 Financial Evidence"
            )


            st.write(
                f"**Invoice Amount:** "
                f"₹{safe_number(row.get('amount_invoice', 0)):,.0f}"
            )


            st.write(
                f"**Payment Amount:** "
                f"₹{safe_number(row.get('amount_payment', 0)):,.0f}"
            )


            st.write(
                f"**Refund Amount:** "
                f"₹{safe_number(row.get('refund_amount', 0)):,.0f}"
            )


            st.write(
                f"**Accounting Expense:** "
                f"₹{safe_number(row.get('recorded_expense', 0)):,.0f}"
            )


            st.write(
                f"**Expected Expense:** "
                f"₹{safe_number(row.get('expected_expense', 0)):,.0f}"
            )


            st.write(
                f"**Accounting Difference:** "
                f"₹{safe_number(row.get('accounting_difference', 0)):,.0f}"
            )


            # ------------------------------------------------
            # INVESTIGATION EXPLANATION
            # ------------------------------------------------

            st.markdown(
                "### 📝 Investigation Explanation"
            )


            st.info(
                explanation
            )


            # ------------------------------------------------
            # RECOMMENDED ACTION
            # ------------------------------------------------

            st.markdown(
                "### 💡 Recommended Action"
            )


            if anomaly_type.upper() == "NO ANOMALY":

                st.success(
                    recommendation
                )

            else:

                st.warning(
                    recommendation
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "FinTrace AI — Automated Financial Reconciliation, "
    "Anomaly Detection & Investigation"
)

