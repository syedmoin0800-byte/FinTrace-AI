import pandas as pd

from src.reconciliation import reconcile_financial_records


def test_reconciled_transaction():

    invoices = pd.DataFrame([
        {
            "invoice_id": "INV001",
            "vendor": "Test Vendor",
            "department": "Test",
            "amount": 100000,
            "date": "2026-08-01"
        }
    ])

    payments = pd.DataFrame([
        {
            "payment_id": "PAY001",
            "invoice_id": "INV001",
            "amount": 100000,
            "status": "Success",
            "date": "2026-08-02"
        }
    ])

    refunds = pd.DataFrame([
        {
            "refund_id": "REF001",
            "payment_id": "PAY001",
            "amount": 0,
            "reason": "No refund",
            "date": "2026-08-02"
        }
    ])

    accounting = pd.DataFrame([
        {
            "entry_id": "ACC001",
            "invoice_id": "INV001",
            "recorded_expense": 100000,
            "date": "2026-08-02"
        }
    ])

    result = reconcile_financial_records(
        invoices,
        payments,
        refunds,
        accounting
    )

    assert len(result) == 1
    assert result.iloc[0]["reconciliation_status"] == "RECONCILED"
    assert result.iloc[0]["accounting_difference"] == 0


def test_unreconciled_refund():

    invoices = pd.DataFrame([
        {
            "invoice_id": "INV002",
            "vendor": "Test Vendor",
            "department": "Test",
            "amount": 500000,
            "date": "2026-08-01"
        }
    ])

    payments = pd.DataFrame([
        {
            "payment_id": "PAY002",
            "invoice_id": "INV002",
            "amount": 500000,
            "status": "Success",
            "date": "2026-08-02"
        }
    ])

    refunds = pd.DataFrame([
        {
            "refund_id": "REF002",
            "payment_id": "PAY002",
            "amount": 100000,
            "reason": "Customer refund",
            "date": "2026-08-03"
        }
    ])

    accounting = pd.DataFrame([
        {
            "entry_id": "ACC002",
            "invoice_id": "INV002",
            "recorded_expense": 500000,
            "date": "2026-08-03"
        }
    ])

    result = reconcile_financial_records(
        invoices,
        payments,
        refunds,
        accounting
    )

    assert len(result) == 1
    assert result.iloc[0]["reconciliation_status"] == "UNRECONCILED"
    assert result.iloc[0]["accounting_difference"] == 100000
    assert result.iloc[0]["issue_type"] == "UNRECONCILED REFUND"


def test_full_refund_mismatch():

    invoices = pd.DataFrame([
        {
            "invoice_id": "INV003",
            "vendor": "Test Vendor",
            "department": "Test",
            "amount": 300000,
            "date": "2026-08-01"
        }
    ])

    payments = pd.DataFrame([
        {
            "payment_id": "PAY003",
            "invoice_id": "INV003",
            "amount": 300000,
            "status": "Success",
            "date": "2026-08-02"
        }
    ])

    refunds = pd.DataFrame([
        {
            "refund_id": "REF003",
            "payment_id": "PAY003",
            "amount": 300000,
            "reason": "Full refund",
            "date": "2026-08-03"
        }
    ])

    accounting = pd.DataFrame([
        {
            "entry_id": "ACC003",
            "invoice_id": "INV003",
            "recorded_expense": 300000,
            "date": "2026-08-03"
        }
    ])

    result = reconcile_financial_records(
        invoices,
        payments,
        refunds,
        accounting
    )

    row = result.iloc[0]

    assert row["refund_amount"] == 300000
    assert row["expected_expense"] == 0
    assert row["accounting_difference"] == 300000
    assert row["reconciliation_status"] == "UNRECONCILED"
    assert row["issue_type"] == "UNRECONCILED REFUND"


def test_missing_payment():

    invoices = pd.DataFrame([
        {
            "invoice_id": "INV004",
            "vendor": "Test Vendor",
            "department": "Test",
            "amount": 750000,
            "date": "2026-08-01"
        }
    ])

    payments = pd.DataFrame(columns=[
        "payment_id",
        "invoice_id",
        "amount",
        "status",
        "date"
    ])

    refunds = pd.DataFrame(columns=[
        "refund_id",
        "payment_id",
        "amount",
        "reason",
        "date"
    ])

    accounting = pd.DataFrame([
        {
            "entry_id": "ACC004",
            "invoice_id": "INV004",
            "recorded_expense": 750000,
            "date": "2026-08-02"
        }
    ])

    result = reconcile_financial_records(
        invoices,
        payments,
        refunds,
        accounting
    )

    row = result.iloc[0]

    assert row["payment_status"] == "PAYMENT MISSING"