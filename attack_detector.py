import pandas as pd

df = pd.read_csv("data/vehicle_data.csv")

attacks = []

for index, row in df.iterrows():

    attack_detected = False

    if row["Speed"] > 200:
        attack_detected = True

    if row["RPM"] > 7000:
        attack_detected = True

    if attack_detected:

        if row["Speed"] > 800:
            severity = "CRITICAL"
        elif row["Speed"] > 500:
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        row_data = row.to_dict()
        row_data["Severity"] = severity

        attacks.append(row_data)

attack_df = pd.DataFrame(attacks)

attack_df.to_csv("data/attack_log.csv", index=False)

print(f"Total attacks detected: {len(attacks)}")