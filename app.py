import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="6G Smart Factory Dashboard", layout="wide")
st.title("🏭 6G Smart Factory Monitoring Dashboard")
st.write("Real-time Industrial IoT Sensor Data Analytics")

@st.cache_data
def load_data():
    df = pd.read_csv("../data/factory_data.csv")  # Folder path update kiya hai
    df['Defect_Density_Score'] = df['Quality_Control_Defect_Rate_%'] / df['Production_Speed_units_per_hr']
    df['Machine_Health_Index'] = 100 - (df['Temperature_C'] * 0.3 + df['Vibration_Hz'] * 0.5)
    df['Machine_Health_Index'] = df['Machine_Health_Index'].clip(0, 100)
    return df

df = load_data()

st.sidebar.header("Filter Options")
selected_machine = st.sidebar.selectbox("Select Machine ID", df['Machine_ID'].unique())
filtered_df = df[df['Machine_ID'] == selected_machine]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Temperature (°C)", f"{filtered_df['Temperature_C'].mean():.2f}")
with col2:
    st.metric("Avg Machine Health Index", f"{filtered_df['Machine_Health_Index'].mean():.2f}")
with col3:
    st.metric("Avg Production Speed (units/hr)", f"{int(filtered_df['Production_Speed_units_per_hr'].mean())}")

st.markdown("---")
col4, col5 = st.columns(2)
with col4:
    st.subheader("Temperature vs Vibration Trend")
    fig1 = px.scatter(filtered_df, x="Temperature_C", y="Vibration_Hz", color="Operation_Mode")
    st.plotly_chart(fig1, use_container_width=True)
with col5:
    st.subheader("Network Latency over Time (6G Performance)")
    fig2 = px.line(filtered_df, x="Time", y="Network_Latency_ms")
    st.plotly_chart(fig2, use_container_width=True)