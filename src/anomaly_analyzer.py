import pandas as pd


def analyze_anomaly(row):
    """
    Analyze a reconciled transaction and classify
    the financial anomaly.
    """

    difference = abs(row["accounting_difference"])
    refund_amount = row["refund_amount"]

    # No anomaly
    if difference == 0:
        return {
            "anomaly_type": "NO ANOMALY",
            "severity": "LOW",
            "financial_impact": 0,
            "reason": "All financial records are reconciled.",
        }

    # Refund-related anomaly
    if refund_amount > 0 and difference > 0:

        # Severity based on financial impact
        if difference >= 1000000:
            severity = "CRITICAL"
        elif difference >= 100000:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        return {
            "anomaly_type": "UNRECONCILED REFUND",
            "severity": severity,
            "financial_impact": difference,
            "reason": (
                "A refund exists, but the accounting record "
                "does not reflect the corresponding reduction "
                "in expense."
            ),
        }

    # Generic accounting mismatch
    if difference > 0:

        if difference >= 1000000:
            severity = "CRITICAL"
        elif difference >= 100000:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        return {
            "anomaly_type": "ACCOUNTING MISMATCH",
            "severity": severity,
            "financial_impact": difference,
            "reason": (
                "The recorded accounting amount does not "
                "match the expected financial amount."
            ),
        }


def main():

    invoices = pd.read_csv("data/invoices.csv")
    payments = pd.read_csv("data/payments.csv")
    refunds = pd.read_csv("data/refunds.csv")
    accounting = pd.read_csv("data/accounting.csv")

    from reconciliation import reconcile_financial_records

    result = reconcile_financial_records(
        invoices,
        payments,
        refunds,
        accounting
    )

    print("\n=== FINTRACE ANOMALY ANALYSIS ===")

    for _, row in result.iterrows():

        analysis = analyze_anomaly(row)

        print("\n----------------------------------------")
        print(f"Invoice: {row['invoice_id']}")
        print(f"Anomaly: {analysis['anomaly_type']}")
        print(f"Severity: {analysis['severity']}")
        print(
            f"Financial Impact: "
            f"₹{analysis['financial_impact']:,.0f}"
        )
        print(f"Reason: {analysis['reason']}")


if __name__ == "__main__":
    main()
    