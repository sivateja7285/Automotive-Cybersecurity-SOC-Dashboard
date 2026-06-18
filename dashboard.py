import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Automotive Cybersecurity SOC",
    layout="wide"
)

# Auto refresh every 2 seconds

st_autorefresh(
    interval=2000,
    key="refresh"
)

# -------------------------------
# Load Data
# -------------------------------

vehicle = pd.read_csv("data/vehicle_data.csv")

# Show latest 500 messages only

vehicle = vehicle.tail(500)
# -------------------------------
# DoS Detection
# -------------------------------

ecu_counts_full = vehicle["CAN_ID"].value_counts()

dos_ecus = ecu_counts_full[
    ecu_counts_full > 20
]
dos_attacks = vehicle[
    vehicle["Attack_Type"] == "DoS Attack"
]


# Live attack detection

attacks = vehicle[
    (vehicle["Speed"] > 200) |
    (vehicle["RPM"] > 7000)
].copy()

# -------------------------------
# Severity Classification
# -------------------------------

def get_severity(row):

    if row["Speed"] > 800 or row["RPM"] > 12000:
        return "CRITICAL"

    elif row["Speed"] > 500 or row["RPM"] > 9000:
        return "HIGH"

    else:
        return "MEDIUM"

if not attacks.empty:

    attacks["Severity"] = attacks.apply(
        get_severity,
        axis=1
    )

# -------------------------------
# Title
# -------------------------------

st.title("Automotive Cybersecurity SOC Dashboard")

# -------------------------------
# Critical Alert Panel
# -------------------------------

critical_alerts = vehicle[
    (vehicle["Speed"] > 800) |
    (vehicle["RPM"] > 12000)
]

if not critical_alerts.empty:

    st.error(
        f"🚨 CRITICAL ALERTS DETECTED: {len(critical_alerts)}"
    )


# -------------------------------
# DoS Detection Panel
# -------------------------------
st.divider()
st.subheader("🚨 DoS Attack Detection")

if not dos_attacks.empty:

    st.error(
        f"🚨 DoS Attack Events Detected: {len(dos_attacks)}"
    )

    st.dataframe(
        dos_attacks[
            [
                "Timestamp",
                "CAN_ID",
                "Speed",
                "RPM",
                "Temperature"
            ]
        ].tail(10)
    )

else:

    st.success(
        "No DoS Attack Detected"
    )

# -------------------------------
# Metrics
# -------------------------------

total_messages = len(vehicle)
total_attacks = len(attacks)

attack_rate = round(
    (total_attacks / total_messages) * 100,
    2
)

replay_count = len(
    vehicle[
        vehicle["Attack_Type"] == "Replay Attack"
    ]
)

dos_count = len(
    vehicle[
        vehicle["Attack_Type"] == "DoS Attack"
    ]
)

critical_count = len(critical_alerts)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "CAN Msgs",
        total_messages
    )

with col2:
    st.metric(
        "Threats",
        total_attacks
    )

with col3:
    st.metric(
        "Replay",
        replay_count
    )

with col4:
    st.metric(
        "DoS",
        dos_count
    )

with col5:
    st.metric(
        "Critical",
        critical_count
    )

with col6:
    st.metric(
        "Attack %",
        attack_rate
    )
# -------------------------------
# Vehicle Telemetry
# -------------------------------
st.divider()
st.subheader("🚗 Vehicle Telemetry")

st.dataframe(vehicle)

# -------------------------------
# Detected Threats
# -------------------------------
st.divider()
st.subheader("🚨 Detected Threats")

st.dataframe(attacks)

# -------------------------------
# Speed Analysis Graph
# -------------------------------
st.divider()
st.subheader("📈 Vehicle Speed Analysis")

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(vehicle["Speed"])

ax.set_xlabel("CAN Message Number")
ax.set_ylabel("Speed")

st.pyplot(fig)

# -------------------------------
# ECU Traffic Distribution
# -------------------------------
st.divider()
st.subheader("🚗 ECU Traffic Distribution")

ecu_counts = vehicle["CAN_ID"].value_counts()

st.bar_chart(ecu_counts)

# -------------------------------
# Attack Type Distribution
# -------------------------------
st.divider()
st.subheader("🎯 Attack Type Distribution")

attack_counts = vehicle["Attack_Type"].value_counts()

st.bar_chart(attack_counts)

# -------------------------------
# Severity Distribution
# -------------------------------
st.divider()
st.subheader("🚨 Attack Severity Distribution")

if not attacks.empty:

    severity_counts = attacks["Severity"].value_counts()

    st.bar_chart(severity_counts)

else:

    st.success(
        "No attacks detected."
    )

# -------------------------------
# Replay Attack Detection
# -------------------------------

st.divider()
st.subheader("🔁 Replay Attack Detection")

# Detect replay attacks directly
replay_attacks = vehicle[
    vehicle["Attack_Type"] == "Replay Attack"
]

if not replay_attacks.empty:

    st.warning(
        f"Replay Attack Events: {len(replay_attacks)}"
    )

    st.dataframe(
        replay_attacks[
            [
                "Timestamp",
                "CAN_ID",
                "Speed",
                "RPM",
                "Temperature",
                "Attack_Type"
            ]
        ]
    )

else:

    st.success(
        "No Replay Attacks Detected"
    )
# -------------------------------
# DoS Traffic Analysis
# -------------------------------
st.divider()
st.subheader("📊 ECU Traffic Volume Analysis")

ecu_counts = vehicle["CAN_ID"].value_counts()

st.bar_chart(ecu_counts)