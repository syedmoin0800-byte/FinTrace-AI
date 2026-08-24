import pandas as pd


def validate_data(df, name, id_column):
    print(f"\n=== {name} VALIDATION ===")

    # Missing values
    missing = df.isnull().sum()

    if missing.sum() == 0:
        print("✅ No missing values")
    else:
        print("⚠️ Missing values found:")
        print(missing[missing > 0])

    # Duplicate IDs
    duplicates = df[id_column].duplicated().sum()

    if duplicates == 0:
        print("✅ No duplicate IDs")
    else:
        print(f"⚠️ {duplicates} duplicate ID(s) found")

    # Negative amounts
    if "amount" in df.columns:
        negative_amounts = (df["amount"] < 0).sum()

        if negative_amounts == 0:
            print("✅ No negative amounts")
        else:
            print(f"⚠️ {negative_amounts} negative amount(s) found")


def main():
    invoices = pd.read_csv("data/invoices.csv")
    payments = pd.read_csv("data/payments.csv")
    refunds = pd.read_csv("data/refunds.csv")
    accounting = pd.read_csv("data/accounting.csv")

    validate_data(invoices, "INVOICES", "invoice_id")
    validate_data(payments, "PAYMENTS", "payment_id")
    validate_data(refunds, "REFUNDS", "refund_id")
    validate_data(accounting, "ACCOUNTING", "entry_id")


if __name__ == "__main__":
    main()