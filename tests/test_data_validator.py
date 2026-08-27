import pandas as pd

from src.data_validator import validate_data


def test_no_missing_values(capsys):

    df = pd.DataFrame([
        {
            "invoice_id": "INV001",
            "amount": 100000
        }
    ])

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "No missing values" in output


def test_missing_values(capsys):

    df = pd.DataFrame([
        {
            "invoice_id": "INV002",
            "amount": None
        }
    ])

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "Missing values found" in output


def test_duplicate_ids(capsys):

    df = pd.DataFrame([
        {
            "invoice_id": "INV003",
            "amount": 100000
        },
        {
            "invoice_id": "INV003",
            "amount": 150000
        }
    ])

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "1 duplicate ID(s) found" in output


def test_negative_amount(capsys):

    df = pd.DataFrame([
        {
            "invoice_id": "INV004",
            "amount": -50000
        }
    ])

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "1 negative amount(s) found" in output


def test_duplicate_payment_ids(capsys):

    df = pd.DataFrame([
        {
            "payment_id": "PAY001",
            "amount": 100000
        },
        {
            "payment_id": "PAY001",
            "amount": 150000
        }
    ])

    validate_data(
        df,
        "PAYMENTS",
        "payment_id"
    )

    output = capsys.readouterr().out

    assert "1 duplicate ID(s) found" in output


def test_missing_required_column(capsys):

    df = pd.DataFrame([
        {
            "amount": 100000
        }
    ])

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "Required column 'invoice_id' is missing" in output
def test_zero_amount(capsys):

    df = pd.DataFrame([
        {
            "invoice_id": "INV005",
            "amount": 0
        }
    ])

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "No negative amounts" in output
def test_invalid_amount(capsys):

    df = pd.DataFrame([
        {
            "invoice_id": "INV006",
            "amount": "INVALID"
        }
    ])

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "1 invalid amount(s) found" in output
def test_empty_dataset(capsys):

    df = pd.DataFrame(
        columns=[
            "invoice_id",
            "amount"
        ]
    )

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "No missing values" in output
    assert "No duplicate IDs" in output
    assert "No negative amounts" in output
def test_missing_id_value(capsys):

    df = pd.DataFrame([
        {
            "invoice_id": None,
            "amount": 100000
        }
    ])

    validate_data(
        df,
        "INVOICES",
        "invoice_id"
    )

    output = capsys.readouterr().out

    assert "Missing values found" in output