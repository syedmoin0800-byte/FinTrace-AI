import pandas as pd


def load_financial_data():
    invoices = pd.read_csv("data/invoices.csv")
    payments = pd.read_csv("data/payments.csv")
    refunds = pd.read_csv("data/refunds.csv")
    accounting = pd.read_csv("data/accounting.csv")

    return invoices, payments, refunds, accounting


if __name__ == "__main__":
    invoices, payments, refunds, accounting = load_financial_data()

    print("=== INVOICES ===")
    print(invoices)

    print("\n=== PAYMENTS ===")
    print(payments)

    print("\n=== REFUNDS ===")
    print(refunds)

    print("\n=== ACCOUNTING ===")
    print(accounting)