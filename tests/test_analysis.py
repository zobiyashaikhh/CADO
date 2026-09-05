import pandas as pd

from app.analysis import (
    calculate_total_cost,
    calculate_daily_cost,
    calculate_daily_statistics,
    calculate_daily_change,
    calculate_service_cost,
    calculate_service_percentage,
    calculate_monthly_cost,
    calculate_rolling_average,
    calculate_rolling_std,
    calculate_z_score,
    detect_daily_anomalies,
    detect_service_anomalies
)


def create_test_data():
    return pd.DataFrame({
        "date": pd.to_datetime([
            "2026-08-01",
            "2026-08-01",
            "2026-08-02",
            "2026-08-02",
            "2026-08-03",
            "2026-08-03"
        ]),
        "service": [
            "EC2",
            "S3",
            "EC2",
            "S3",
            "EC2",
            "S3"
        ],
        "cost": [
            100,
            50,
            200,
            100,
            150,
            75
        ]
    })


def test_total_cost():
    df = create_test_data()
    result = calculate_total_cost(df)
    assert result == 675


def test_daily_cost():
    df = create_test_data()
    result = calculate_daily_cost(df)

    assert result.iloc[0] == 150
    assert result.iloc[1] == 300
    assert result.iloc[2] == 225


def test_daily_statistics():
    df = create_test_data()
    daily_cost = calculate_daily_cost(df)

    average, minimum, maximum = calculate_daily_statistics(
        daily_cost
    )

    assert average == 225
    assert minimum == 150
    assert maximum == 300


def test_daily_change():
    df = create_test_data()
    daily_cost = calculate_daily_cost(df)
    result = calculate_daily_change(daily_cost)

    assert pd.isna(result.iloc[0])
    assert round(result.iloc[1], 2) == 100.00
    assert round(result.iloc[2], 2) == -25.00


def test_service_cost():
    df = create_test_data()
    result = calculate_service_cost(df)

    assert result["EC2"] == 450
    assert result["S3"] == 225


def test_service_percentage():
    service_cost = pd.Series({
        "EC2": 450,
        "S3": 225
    })

    result = calculate_service_percentage(
        service_cost,
        675
    )

    assert round(result["EC2"], 2) == 66.67
    assert round(result["S3"], 2) == 33.33


def test_monthly_cost():
    df = create_test_data()
    result = calculate_monthly_cost(df)

    assert result.iloc[0] == 675


def test_rolling_average():
    df = create_test_data()
    daily_cost = calculate_daily_cost(df)
    result = calculate_rolling_average(daily_cost)

    assert result.iloc[0] == 150
    assert result.iloc[1] == 225


def test_rolling_std():
    df = create_test_data()
    daily_cost = calculate_daily_cost(df)
    result = calculate_rolling_std(daily_cost)

    assert pd.isna(result.iloc[0])
    assert round(result.iloc[1], 2) == 106.07


def test_z_score():
    df = create_test_data()
    daily_cost = calculate_daily_cost(df)
    result = calculate_z_score(daily_cost)

    assert len(result) == 3


def test_daily_anomaly_detection():
    df = create_test_data()
    daily_cost = calculate_daily_cost(df)

    result = detect_daily_anomalies(
        daily_cost,
        threshold=2
    )

    assert "actual_cost" in result.columns
    assert "z_score" in result.columns
    assert "is_anomaly" in result.columns


def test_service_anomaly_detection():
    df = create_test_data()

    result = detect_service_anomalies(
        df,
        threshold=2
    )

    assert isinstance(result, pd.DataFrame)