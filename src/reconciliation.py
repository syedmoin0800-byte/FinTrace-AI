import pandas as pd


def reconcile_financial_records(invoices, payments, refunds, accounting):

    # -------------------------------------------------
    # STEP 1: Invoice ↔ Payment Reconciliation
    # -------------------------------------------------

    invoice_payment = invoices.merge(
        payments,
        on="invoice_id",
        how="left",
        suffixes=("_invoice", "_payment")
    )

    invoice_payment["payment_difference"] = (
        invoice_payment["amount_invoice"]
        - invoice_payment["amount_payment"]
    )

    invoice_payment["payment_status"] = "MATCHED"

    invoice_payment.loc[
        invoice_payment["amount_payment"].isna(),
        "payment_status"
    ] = "PAYMENT MISSING"

    invoice_payment.loc[
        (invoice_payment["amount_payment"].notna()) &
        (invoice_payment["payment_difference"] != 0),
        "payment_status"
    ] = "AMOUNT MISMATCH"


    # -------------------------------------------------
    # STEP 2: Payment ↔ Refund Reconciliation
    # -------------------------------------------------

    payment_refund = payments.merge(
        refunds,
        on="payment_id",
        how="left",
        suffixes=("_payment", "_refund")
    )

    payment_refund["refund_amount"] = (
        payment_refund["amount_refund"].fillna(0)
    )

    payment_refund["net_paid_amount"] = (
        payment_refund["amount_payment"]
        - payment_refund["refund_amount"]
    )


    # -------------------------------------------------
    # STEP 3: Connect Accounting Records
    # -------------------------------------------------

    final_result = invoice_payment.merge(
        payment_refund[
            [
                "payment_id",
                "refund_id",
                "refund_amount",
                "net_paid_amount",
                "reason"
            ]
        ],
        on="payment_id",
        how="left"
    )

    final_result = final_result.merge(
        accounting[
            [
                "invoice_id",
                "recorded_expense"
            ]
        ],
        on="invoice_id",
        how="left"
    )


    # -------------------------------------------------
    # STEP 4: Calculate Expected Expense
    # -------------------------------------------------

    final_result["refund_amount"] = (
        final_result["refund_amount"].fillna(0)
    )

    final_result["expected_expense"] = (
        final_result["amount_payment"]
        - final_result["refund_amount"]
    )


    # -------------------------------------------------
    # STEP 5: Detect Accounting Mismatch
    # -------------------------------------------------

    final_result["accounting_difference"] = (
        final_result["recorded_expense"]
        - final_result["expected_expense"]
    )

    final_result["reconciliation_status"] = "RECONCILED"

    final_result.loc[
        final_result["accounting_difference"] != 0,
        "reconciliation_status"
    ] = "UNRECONCILED"


    # -------------------------------------------------
    # STEP 6: Explain the Issue
    # -------------------------------------------------

    final_result["issue_type"] = "NO ISSUE"

    refund_issue = (
        (final_result["refund_amount"] > 0) &
        (final_result["accounting_difference"] != 0)
    )

    final_result.loc[
        refund_issue,
        "issue_type"
    ] = "UNRECONCILED REFUND"


    return final_result


def main():

    # Load financial records

    invoices = pd.read_csv("data/invoices.csv")
    payments = pd.read_csv("data/payments.csv")
    refunds = pd.read_csv("data/refunds.csv")
    accounting = pd.read_csv("data/accounting.csv")


    # Run reconciliation

    result = reconcile_financial_records(
        invoices,
        payments,
        refunds,
        accounting
    )


    # Display important results

    print("\n=== FINTRACE FINANCIAL RECONCILIATION ===")

    print(
        result[
            [
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
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()