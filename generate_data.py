import pandas as pd
import numpy as np

np.random.seed(42)

dates = pd.date_range("2026-08-01", "2026-08-30")

services = {
    "EC2": (1200, "Compute"),
    "S3": (350, "Storage"),
    "RDS": (800, "Database"),
    "Lambda": (200, "Compute"),
    "CloudFront": (300, "Data Transfer"),
    "DynamoDB": (250, "Database")
}

regions = [
    "ap-south-1",
    "us-east-1",
    "ap-southeast-1"
]

data = []

for date in dates:
    for service, (base_cost, usage_type) in services.items():

        cost = np.random.normal(
            base_cost,
            base_cost * 0.08
        )

        region = np.random.choice(regions)

        data.append({
            "date": date,
            "service": service,
            "region": region,
            "usage_type": usage_type,
            "cost": round(max(cost, 0), 2),
            "currency": "INR"
        })


df = pd.DataFrame(data)

# Plant intentional anomalies
df.loc[
    (df["date"] == "2026-08-10") &
    (df["service"] == "EC2"),
    "cost"
] = 4800

df.loc[
    (df["date"] == "2026-08-17") &
    (df["service"] == "RDS"),
    "cost"
] = 3200

df.loc[
    (df["date"] == "2026-08-23") &
    (df["service"] == "S3"),
    "cost"
] = 1800

df.loc[
    (df["date"] == "2026-08-27") &
    (df["service"] == "DynamoDB"),
    "cost"
] = 1200

df.to_csv("data/billing.csv", index=False)

print("Billing dataset generated successfully!")
print(f"Records: {len(df)}")