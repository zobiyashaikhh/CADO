import matplotlib.pyplot as plt

from ingestion import load_billing_data, clean_billing_data
from analysis import (
    calculate_daily_cost,
    calculate_service_cost,
    calculate_rolling_average,
    detect_service_anomalies
)


df = load_billing_data("data/billing.csv")
df = clean_billing_data(df)

daily_cost = calculate_daily_cost(df)
service_cost = calculate_service_cost(df)
rolling_average = calculate_rolling_average(daily_cost)
service_anomalies = detect_service_anomalies(df)


plt.figure(figsize=(12, 6))
plt.plot(daily_cost.index, daily_cost.values, marker="o")
plt.title("Daily Cloud Spending")
plt.xlabel("Date")
plt.ylabel("Cost")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("daily_spending.png")
plt.close()


plt.figure(figsize=(10, 6))
plt.bar(service_cost.index, service_cost.values)
plt.title("Cloud Cost by Service")
plt.xlabel("Service")
plt.ylabel("Total Cost")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("service_cost.png")
plt.close()


plt.figure(figsize=(12, 6))
plt.plot(
    daily_cost.index,
    daily_cost.values,
    marker="o",
    label="Actual Cost"
)

plt.plot(
    rolling_average.index,
    rolling_average.values,
    label="7-Day Moving Average"
)

plt.title("Actual Cost vs 7-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Cost")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("actual_vs_average.png")
plt.close()


plt.figure(figsize=(12, 6))
plt.plot(
    daily_cost.index,
    daily_cost.values,
    marker="o",
    label="Daily Cost"
)

for _, row in service_anomalies.iterrows():
    date = row["date"]
    daily_value = daily_cost.loc[date]

    plt.scatter(
        date,
        daily_value,
        s=100,
        label=f"{row['service']} anomaly"
    )

plt.title("Cloud Spending Anomalies")
plt.xlabel("Date")
plt.ylabel("Cost")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("anomalies.png")
plt.close()

print("Visualization completed successfully.")
print("Charts saved:")
print("- daily_spending.png")
print("- service_cost.png")
print("- actual_vs_average.png")
print("- anomalies.png")