import random
import pandas as pd
from datetime import datetime

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

for i in range(100):

    ecu = random.choice(ecus)

    attack = random.random() < 0.1

    speed = random.randint(20, 120)
    rpm = random.randint(1000, 6000)
    temperature = random.randint(70, 110)

    attack_type = "Normal"

    if attack:

        attack_type = random.choice(attack_types)

        if attack_type == "Speed Spoofing":
            speed = random.randint(300, 999)

        elif attack_type == "RPM Manipulation":
            rpm = random.randint(8000, 15000)

        elif attack_type == "Replay Attack":
            speed = random.randint(20, 120)

        elif attack_type == "DoS Attack":
            speed = random.randint(300, 999)

    vehicle_data.append([
        datetime.now(),
        ecu,
        speed,
        rpm,
        temperature,
        attack_type
    ])

df = pd.DataFrame(
    vehicle_data,
    columns=[
        "Timestamp",
        "CAN_ID",
        "Speed",
        "RPM",
        "Temperature",
        "Attack_Type"
    ]
)

df.to_csv("vehicle_data.csv", index=False)

print("Vehicle data generated successfully!")