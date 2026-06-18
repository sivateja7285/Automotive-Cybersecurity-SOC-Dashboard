import random
import pandas as pd
import time
from datetime import datetime
import os

# Store previous messages

vehicle_data = []

ecus = [
"Engine_ECU",
"Brake_ECU",
"ABS_ECU",
"Steering_ECU"
]

attack_types = [
"Speed Spoofing",
"RPM Manipulation",
"Replay Attack",
"DoS Attack"
]

# Create CSV if it doesn't exist

if not os.path.exists("data/vehicle_data.csv"):
    df = pd.DataFrame(columns=[
        "Timestamp",
        "CAN_ID",
        "Speed",
        "RPM",
        "Temperature",
        "Attack_Type"
    ])
    df.to_csv("data/vehicle_data.csv", index=False)


print("🚗 Real-time simulator started...")

while True:
    ecu = random.choice(ecus)
    speed = random.randint(20, 120)
    rpm = random.randint(1000, 6000)
    temperature = random.randint(70, 110)

    attack_type = "Normal"

    attack = random.random() < 0.40

    if attack:

        attack_type = random.choices(
            attack_types,
            weights=[40, 35, 20, 5],
            k=1
        )[0]

        

        # Speed Spoofing
        if attack_type == "Speed Spoofing":

            speed = random.randint(300, 999)

        # RPM Manipulation
        elif attack_type == "RPM Manipulation":

            rpm = random.randint(8000, 15000)

        # Replay Attack
        elif attack_type == "Replay Attack":

            if len(vehicle_data) > 0:

                old_message = random.choice(vehicle_data)

                replayed_message = old_message.copy()

                replayed_message[0] = datetime.now()
                replayed_message[5] = "Replay Attack"

                replay_row = pd.DataFrame(
                    [replayed_message],
                    columns=[
                        "Timestamp",
                        "CAN_ID",
                        "Speed",
                        "RPM",
                        "Temperature",
                        "Attack_Type"
                    ]
                )

                replay_row.to_csv(
                    "data/vehicle_data.csv",
                    mode="a",
                    header=False,
                    index=False
                )

                print("🔁 Replay Attack Generated")

                time.sleep(1)

                continue

        # REAL DoS Attack
        elif attack_type == "DoS Attack":

            flood_ecu = random.choice(ecus)

            print(f"🚨 DoS Attack Started from {flood_ecu}")

            for _ in range(25):

                dos_row_data = [
                    datetime.now(),
                    flood_ecu,
                    random.randint(40, 120),
                    random.randint(1000, 4000),
                    random.randint(70, 110),
                    "DoS Attack"
                ]

                vehicle_data.append(dos_row_data)

                dos_row = pd.DataFrame(
                    [dos_row_data],
                    columns=[
                        "Timestamp",
                        "CAN_ID",
                        "Speed",
                        "RPM",
                        "Temperature",
                        "Attack_Type"
                    ]
                )

                dos_row.to_csv(
                    "data/vehicle_data.csv",
                    mode="a",
                    header=False,
                    index=False
                )

            print(f"🚨 100 Flood Messages Sent from {flood_ecu}")

            time.sleep(1)

            continue

    row_data = [
        datetime.now(),
        ecu,
        speed,
        rpm,
        temperature,
        attack_type
    ]

    vehicle_data.append(row_data)

    row = pd.DataFrame(
        [row_data],
        columns=[
            "Timestamp",
            "CAN_ID",
            "Speed",
            "RPM",
            "Temperature",
            "Attack_Type"
        ]
    )

    row.to_csv(
        "data/vehicle_data.csv",
        mode="a",
        header=False,
        index=False
    )

    print(
        f"{ecu} | Speed={speed} | RPM={rpm} | Temp={temperature} | {attack_type}"
    )

    time.sleep(1)
