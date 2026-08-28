import pandas as pd

try:
    from .data_mapper import map_columns
except ImportError:
    from data_mapper import map_columns

def validate_data(df, name, id_column):

    print(f"\n=== {name} VALIDATION ===")

    # -------------------------------------------------
    # 1. Required ID column check
    # -------------------------------------------------

    if id_column not in df.columns:
        print(f"❌ Required column '{id_column}' is missing")
        return

    print(f"✅ Required ID column '{id_column}' found")

    # -------------------------------------------------
    # 2. Missing values
    # -------------------------------------------------

    missing = df.isnull().sum()

    if missing.sum() == 0:
        print("✅ No missing values")
    else:
        print("⚠️ Missing values found:")

        for column, count in missing[missing > 0].items():
            print(f"   {column}: {count}")

    # -------------------------------------------------
    # 3. Duplicate IDs
    # -------------------------------------------------

    duplicates = df[id_column].duplicated().sum()

    if duplicates == 0:
        print("✅ No duplicate IDs")
    else:
        print(f"⚠️ {duplicates} duplicate ID(s) found")

    # -------------------------------------------------
    # 4. Amount / Expense validation
    # -------------------------------------------------

    # Normal financial amount column
    if "amount" in df.columns:

        numeric_amounts = pd.to_numeric(
            df["amount"],
            errors="coerce"
        )

        invalid_amounts = numeric_amounts.isna().sum()

        if invalid_amounts == 0:
            print("✅ All amounts are numeric")
        else:
            print(
                f"⚠️ {invalid_amounts} invalid amount(s) found"
            )

        negative_amounts = (
            numeric_amounts.dropna() < 0
        ).sum()

        if negative_amounts == 0:
            print("✅ No negative amounts")
        else:
            print(
                f"⚠️ {negative_amounts} negative amount(s) found"
            )

    # Accounting expense column
    elif "recorded_expense" in df.columns:

        numeric_expenses = pd.to_numeric(
            df["recorded_expense"],
            errors="coerce"
        )

        invalid_expenses = numeric_expenses.isna().sum()

        if invalid_expenses == 0:
            print("✅ All recorded expenses are numeric")
        else:
            print(
                f"⚠️ {invalid_expenses} invalid recorded expense(s) found"
            )

        negative_expenses = (
            numeric_expenses.dropna() < 0
        ).sum()

        if negative_expenses == 0:
            print("✅ No negative recorded expenses")
        else:
            print(
                f"⚠️ {negative_expenses} negative recorded expense(s) found"
            )

    else:

        print("ℹ️ No financial amount column to validate")


def main():

    # -------------------------------------------------
    # Load datasets
    # -------------------------------------------------

    invoices = pd.read_csv("data/invoices.csv")
    payments = pd.read_csv("data/payments.csv")
    refunds = pd.read_csv("data/refunds.csv")
    accounting = pd.read_csv("data/accounting.csv")

    # -------------------------------------------------
    # Apply Data Mapper
    # -------------------------------------------------

    invoices = map_columns(invoices)
    payments = map_columns(payments)
    refunds = map_columns(refunds)
    accounting = map_columns(accounting)

    # -------------------------------------------------
    # Display mapped columns
    # -------------------------------------------------

    print("\n=== MAPPED COLUMNS ===")

    print("Invoices:", list(invoices.columns))
    print("Payments:", list(payments.columns))
    print("Refunds:", list(refunds.columns))
    print("Accounting:", list(accounting.columns))

    # -------------------------------------------------
    # Validate datasets
    # -------------------------------------------------

    validate_data(
        invoices,
        "INVOICES",
        "invoice_id"
    )

    validate_data(
        payments,
        "PAYMENTS",
        "payment_id"
    )

    validate_data(
        refunds,
        "REFUNDS",
        "refund_id"
    )

    validate_data(
        accounting,
        "ACCOUNTING",
        "entry_id"
    )


if __name__ == "__main__":
    main()