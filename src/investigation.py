import pandas as pd


def generate_investigation(row):

    invoice_id = row["invoice_id"]
    payment_id = row["payment_id"]

    invoice_amount = row["amount_invoice"]
    payment_amount = row["amount_payment"]
    refund_amount = row["refund_amount"]
    recorded_expense = row["recorded_expense"]
    expected_expense = row["expected_expense"]
    difference = row["accounting_difference"]

    reason = row.get("reason", "Not provided")

    if difference != 0 and refund_amount > 0:

        explanation = (
            f"Invoice {invoice_id} received a payment of "
            f"₹{payment_amount:,.0f} through {payment_id}. "
            f"A refund of ₹{refund_amount:,.0f} was issued "
            f"for reason: {reason}. "
            f"The expected expense after the refund is "
            f"₹{expected_expense:,.0f}, but the accounting record "
            f"still shows ₹{recorded_expense:,.0f}. "
            f"This creates an unreconciled difference of "
            f"₹{difference:,.0f}."
        )

        recommendation = (
            "Review the refund reference and update the accounting "
            "record to reflect the net expense."
        )

    elif difference != 0:

        explanation = (
            f"Invoice {invoice_id} has an accounting difference "
            f"of ₹{difference:,.0f}. "
            f"The recorded expense does not match the expected expense."
        )

        recommendation = (
            "Review the invoice, payment and accounting records "
            "to identify the source of the difference."
        )

    else:

        explanation = (
            f"Invoice {invoice_id} is fully reconciled. "
            f"Payment, refund and accounting records are consistent."
        )

        recommendation = "No action required."

    return explanation, recommendation


def main():

    # Load data
    invoices = pd.read_csv("data/invoices.csv")
    payments = pd.read_csv("data/payments.csv")
    refunds = pd.read_csv("data/refunds.csv")
    accounting = pd.read_csv("data/accounting.csv")

    # Import reconciliation engine
    from reconciliation import reconcile_financial_records

    result = reconcile_financial_records(
        invoices,
        payments,
        refunds,
        accounting
    )

    print("\n=== FINTRACE INVESTIGATION REPORT ===")

    for _, row in result.iterrows():

        explanation, recommendation = generate_investigation(row)

        print("\n----------------------------------------")
        print(f"Invoice: {row['invoice_id']}")
        print(f"Status: {row['reconciliation_status']}")
        print(f"Issue: {row['issue_type']}")
        print("\nExplanation:")
        print(explanation)
        print("\nRecommended Action:")
        print(recommendation)


if __name__ == "__main__":
    main()