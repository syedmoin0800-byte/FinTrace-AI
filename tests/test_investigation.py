from src.investigation import generate_investigation


def test_unreconciled_refund_investigation():

    row = {
        "invoice_id": "INV001",
        "payment_id": "PAY001",
        "amount_invoice": 1800000,
        "amount_payment": 1800000,
        "refund_amount": 450000,
        "recorded_expense": 1800000,
        "expected_expense": 1350000,
        "accounting_difference": 450000,
        "reason": "Production work completed earlier",
        "reconciliation_status": "UNRECONCILED",
        "issue_type": "UNRECONCILED REFUND"
    }

    explanation, recommendation = generate_investigation(row)

    assert "INV001" in explanation
    assert "450,000" in explanation
    assert "1,350,000" in explanation
    assert "1,800,000" in explanation

    assert recommendation != ""


def test_reconciled_transaction_investigation():

    row = {
        "invoice_id": "INV002",
        "payment_id": "PAY002",
        "amount_invoice": 1200000,
        "amount_payment": 1200000,
        "refund_amount": 0,
        "recorded_expense": 1200000,
        "expected_expense": 1200000,
        "accounting_difference": 0,
        "reason": "No refund",
        "reconciliation_status": "RECONCILED",
        "issue_type": "NO ISSUE"
    }

    explanation, recommendation = generate_investigation(row)

    assert "INV002" in explanation
    assert "fully reconciled" in explanation
    assert recommendation == "No action required."