import pandas as pd


# Common column-name patterns
COLUMN_ALIASES = {
    "invoice_id": [
        "invoice_id",
        "invoice",
        "invoice_number",
        "invoice_no",
        "bill_id",
        "bill_number"
    ],

    "payment_id": [
        "payment_id",
        "payment",
        "payment_number",
        "payment_no",
        "transaction_id",
        "transaction_number"
    ],

    "refund_id": [
        "refund_id",
        "refund",
        "refund_number",
        "refund_no"
    ],

    "entry_id": [
        "entry_id",
        "accounting_id",
        "account_id",
        "journal_id",
        "entry_number"
    ],

    "amount": [
        "amount",
        "total_amount",
        "invoice_amount",
        "value",
        "price",
        "total",
        "transaction_amount"
    ],

    "amount_payment": [
        "amount_payment",
        "payment_amount",
        "paid_amount",
        "paid_value"
    ],

    "amount_refund": [
        "amount_refund",
        "refund_amount",
        "refunded_amount",
        "refund_value"
    ],

    "recorded_expense": [
        "recorded_expense",
        "accounting_expense",
        "expense",
        "recorded_amount",
        "accounted_amount"
    ],

    "reason": [
        "reason",
        "refund_reason",
        "description",
        "remarks",
        "comment"
    ]
}


def normalize_column_name(column):
    """
    Convert column names into a comparable format.
    """

    return (
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def map_columns(df):
    """
    Detect common column names and map them
    to FinTrace standard column names.
    """

    mapped_df = df.copy()

    # Normalize original column names
    normalized_columns = {
        column: normalize_column_name(column)
        for column in df.columns
    }

    rename_map = {}

    for original, normalized in normalized_columns.items():

        for standard_name, aliases in COLUMN_ALIASES.items():

            normalized_aliases = [
                normalize_column_name(alias)
                for alias in aliases
            ]

            if normalized in normalized_aliases:

                # Don't overwrite an already detected
                # standard column
                if standard_name not in rename_map.values():
                    rename_map[original] = standard_name

                break

    mapped_df = mapped_df.rename(columns=rename_map)

    return mapped_df


def detect_columns(df):
    """
    Return detected FinTrace standard columns.
    """

    mapped_df = map_columns(df)

    return list(mapped_df.columns)


def main():

    print("\n" + "=" * 60)
    print("FINTRACE DATA MAPPER - REAL DATA TEST")
    print("=" * 60)

    files = {
        "INVOICES": "data/invoices.csv",
        "PAYMENTS": "data/payments.csv",
        "REFUNDS": "data/refunds.csv",
        "ACCOUNTING": "data/accounting.csv"
    }

    for name, path in files.items():

        print("\n" + "-" * 60)
        print(f"{name}")
        print("-" * 60)

        try:
            df = pd.read_csv(path)

            print("\nOriginal columns:")
            print(list(df.columns))

            mapped_df = map_columns(df)

            print("\nMapped columns:")
            print(list(mapped_df.columns))

            print("\nSample data:")
            print(mapped_df.head().to_string(index=False))

        except FileNotFoundError:
            print(f"❌ File not found: {path}")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()