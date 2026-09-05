import pandas as pd


VALID_SERVICES = {
    "EC2",
    "S3",
    "RDS",
    "Lambda",
    "CloudFront",
    "DynamoDB"
}


def load_billing_data(file_path):
    df = pd.read_csv(file_path)
    return df


def clean_billing_data(df):
    df = df.copy()

    # Convert date to datetime
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Convert cost to numeric
    df["cost"] = pd.to_numeric(
        df["cost"],
        errors="coerce"
    )

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove rows with missing critical values
    df = df.dropna(
        subset=["date", "service", "cost"]
    )

    # Keep only valid services
    df = df[
        df["service"].isin(VALID_SERVICES)
    ]

    # Remove negative costs
    df = df[df["cost"] >= 0]

    # Sort by date
    df = df.sort_values("date")

    return df


if __name__ == "__main__":
    df = load_billing_data("data/billing.csv")

    print("Before cleaning:")
    print(df.shape)

    df = clean_billing_data(df)

    print("\nAfter cleaning:")
    print(df.shape)

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nServices:")
    print(df["service"].unique())

    test_data = pd.DataFrame({
        "date": ["2026-08-01", "2026-08-02", "2026-08-02"],
        "service": ["EC2", "INVALID", "EC2"],
        "region": ["ap-south-1", "ap-south-1", "ap-south-1"],
        "usage_type": ["Compute", "Unknown", "Compute"],
        "cost": [1200, 500, -100],
        "currency": ["INR", "INR", "INR"]
    })

    print("\nTesting bad data:")
    print(test_data)

    cleaned_test = clean_billing_data(test_data)

    print("\nAfter cleaning bad data:")
    print(cleaned_test)