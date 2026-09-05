import pandas as pd


def calculate_total_cost(df):
    return df["cost"].sum()


def calculate_daily_cost(df):
    daily_cost = df.groupby("date")["cost"].sum()
    return daily_cost


def calculate_daily_statistics(daily_cost):
    average = daily_cost.mean()
    minimum = daily_cost.min()
    maximum = daily_cost.max()

    return average, minimum, maximum


def calculate_daily_change(daily_cost):
    daily_change = daily_cost.pct_change() * 100
    return daily_change


def calculate_service_cost(df):
    service_cost = df.groupby("service")["cost"].sum()
    return service_cost


def calculate_service_percentage(service_cost, total_cost):
    service_percentage = (service_cost / total_cost) * 100
    return service_percentage


def calculate_monthly_cost(df):
    monthly_cost = (
        df.groupby(df["date"].dt.to_period("M"))["cost"]
        .sum()
    )

    return monthly_cost


def calculate_rolling_average(daily_cost):
    rolling_average = daily_cost.rolling(
        window=7,
        min_periods=1
    ).mean()

    return rolling_average


def calculate_rolling_std(daily_cost):
    rolling_std = daily_cost.rolling(
        window=7,
        min_periods=1
    ).std()

    return rolling_std


def calculate_expected_cost(daily_cost):
    expected_cost = calculate_rolling_average(daily_cost)
    return expected_cost


def calculate_z_score(daily_cost):
    mean = daily_cost.mean()
    std = daily_cost.std()

    if std == 0:
        return pd.Series(0, index=daily_cost.index)

    z_score = (daily_cost - mean) / std

    return z_score


def detect_daily_anomalies(daily_cost, threshold=2):
    z_score = calculate_z_score(daily_cost)

    anomalies = pd.DataFrame({
        "actual_cost": daily_cost,
        "z_score": z_score
    })

    anomalies["expected_cost"] = daily_cost.mean()

    anomalies["deviation"] = (
        anomalies["actual_cost"]
        - anomalies["expected_cost"]
    )

    anomalies["deviation_percentage"] = (
        anomalies["deviation"]
        / anomalies["expected_cost"]
    ) * 100

    anomalies["is_anomaly"] = (
        anomalies["z_score"].abs() >= threshold
    )

    return anomalies


def detect_service_anomalies(df, threshold=2):
    results = []

    for service in df["service"].unique():

        service_df = df[
            df["service"] == service
        ]

        daily_service_cost = (
            service_df
            .groupby("date")["cost"]
            .sum()
        )

        mean = daily_service_cost.mean()
        std = daily_service_cost.std()

        if std == 0 or pd.isna(std):
            continue

        z_score = (
            daily_service_cost - mean
        ) / std

        for date, score in z_score.items():

            actual_cost = daily_service_cost.loc[date]

            deviation = actual_cost - mean

            deviation_percentage = (
                deviation / mean
            ) * 100

            if abs(score) >= threshold:

                if abs(score) >= 4:
                    severity = "CRITICAL"

                elif abs(score) >= 3:
                    severity = "HIGH"

                else:
                    severity = "MEDIUM"

                results.append({
                    "date": date,
                    "service": service,
                    "actual_cost": actual_cost,
                    "expected_cost": mean,
                    "deviation": deviation,
                    "deviation_percentage": deviation_percentage,
                    "z_score": score,
                    "severity": severity
                })

    if not results:
        return pd.DataFrame(
            columns=[
                "date",
                "service",
                "actual_cost",
                "expected_cost",
                "deviation",
                "deviation_percentage",
                "z_score",
                "severity"
            ]
        )

    return pd.DataFrame(results).sort_values("date")


if __name__ == "__main__":
    from ingestion import load_billing_data, clean_billing_data

    df = load_billing_data("data/billing.csv")
    df = clean_billing_data(df)

    total = calculate_total_cost(df)
    daily_cost = calculate_daily_cost(df)

    average, minimum, maximum = calculate_daily_statistics(
        daily_cost
    )

    daily_change = calculate_daily_change(daily_cost)

    service_cost = calculate_service_cost(df)

    service_percentage = calculate_service_percentage(
        service_cost,
        total
    )

    monthly_cost = calculate_monthly_cost(df)

    rolling_average = calculate_rolling_average(
        daily_cost
    )

    rolling_std = calculate_rolling_std(
        daily_cost
    )

    daily_anomalies = detect_daily_anomalies(
        daily_cost,
        threshold=2
    )

    service_anomalies = detect_service_anomalies(
        df,
        threshold=2
    )

    print("=" * 60)
    print("CADO - CLOUD COST ANALYSIS")
    print("=" * 60)

    print("\nTOTAL CLOUD COST")
    print("-" * 60)
    print(f"₹{total:.2f}")

    print("\nDAILY COST")
    print("-" * 60)
    print(daily_cost)

    print("\nDAILY STATISTICS")
    print("-" * 60)
    print(f"Average Daily Cost : ₹{average:.2f}")
    print(f"Minimum Daily Cost : ₹{minimum:.2f}")
    print(f"Maximum Daily Cost : ₹{maximum:.2f}")

    print("\nDAILY PERCENTAGE CHANGE")
    print("-" * 60)
    print(daily_change)

    print("\nSERVICE-WISE COST")
    print("-" * 60)
    print(service_cost)

    print("\nSERVICE PERCENTAGE OF TOTAL")
    print("-" * 60)
    print(service_percentage)

    print("\nMONTHLY COST")
    print("-" * 60)
    print(monthly_cost)

    print("\n7-DAY MOVING AVERAGE")
    print("-" * 60)
    print(rolling_average)

    print("\n7-DAY ROLLING STANDARD DEVIATION")
    print("-" * 60)
    print(rolling_std)

    print("\nDAILY ANOMALY ANALYSIS")
    print("-" * 60)
    print(
        daily_anomalies[
            daily_anomalies["is_anomaly"]
        ]
    )

    print("\nSERVICE-WISE ANOMALY DETECTION")
    print("-" * 60)

    if service_anomalies.empty:
        print("No anomalies detected.")
    else:
        print(
            service_anomalies.to_string(
                index=False
            )
        )

    print("\n" + "=" * 60)
    print("CADO ANALYSIS SUMMARY")
    print("=" * 60)

    print(f"Total Cost       : ₹{total:.2f}")
    print(f"Average Daily    : ₹{average:.2f}")
    print(f"Minimum Daily    : ₹{minimum:.2f}")
    print(f"Maximum Daily    : ₹{maximum:.2f}")
    print(f"Anomalies Found  : {len(service_anomalies)}")

    if not service_anomalies.empty:
        print("\nDetected Anomalies:")

        for _, row in service_anomalies.iterrows():
            print(
                f"- {row['date'].date()} | "
                f"{row['service']} | "
                f"₹{row['actual_cost']:.2f} | "
                f"{row['severity']}"
            )

    print("\nAnalysis completed successfully.")