from src.anomaly_analyzer import analyze_anomaly


def test_unreconciled_refund():

    row = {
        "accounting_difference": 450000,
        "refund_amount": 450000
    }

    result = analyze_anomaly(row)

    assert result["anomaly_type"] == "UNRECONCILED REFUND"
    assert result["severity"] == "HIGH"
    assert result["financial_impact"] == 450000


def test_no_anomaly():

    row = {
        "accounting_difference": 0,
        "refund_amount": 0
    }

    result = analyze_anomaly(row)

    assert result["anomaly_type"] == "NO ANOMALY"
    assert result["severity"] == "LOW"
    assert result["financial_impact"] == 0


def test_critical_refund_anomaly():

    row = {
        "accounting_difference": 1500000,
        "refund_amount": 1500000
    }

    result = analyze_anomaly(row)

    assert result["anomaly_type"] == "UNRECONCILED REFUND"
    assert result["severity"] == "CRITICAL"
    assert result["financial_impact"] == 1500000


def test_accounting_mismatch():

    row = {
        "accounting_difference": 250000,
        "refund_amount": 0
    }

    result = analyze_anomaly(row)

    assert result["anomaly_type"] == "ACCOUNTING MISMATCH"
    assert result["severity"] == "HIGH"
    assert result["financial_impact"] == 250000