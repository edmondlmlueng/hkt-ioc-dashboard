import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HKT Smart Site IOC", page_icon="🛡️", layout="wide")

st.title("🛡️ HKT Smart Site Integrated Operations Centre (IOC)")
st.subheader("Real-Time Safety Compliance & Analytics Terminal")
st.markdown("---")

with st.sidebar:
    st.header("Site Telemetry")
    st.metric("Active Cameras", "4 / 4")
    st.metric("Alert Status", "ALARM ACTIVE", "-2 Violations")
    st.info("Location: Kowloon District, HK")

col_video, col_logs, col_genai = st.columns([4, 3, 4])

with col_video:
    st.header("📹 CCTV Live Feed")
    st.info("Demo Mode")
    st.image("https://picsum.photos/id/1015/800/450", use_container_width=True, caption="Live Feed (Demo)")

with col_logs:
    st.header("🚨 Latest Alerts")
    if "logs" not in st.session_state:
        st.session_state.logs = pd.DataFrame([
            {"Time": "09:15", "Zone": "Area A", "Event": "Missing Hard Hat"},
        ])
    st.dataframe(st.session_state.logs, use_container_width=True)
    if st.button("Simulate New Alert"):
        new = {"Time": datetime.now().strftime("%H:%M"), "Zone": "Zone B", "Event": "PPE Violation"}
        st.session_state.logs = pd.concat([st.session_state.logs, pd.DataFrame([new])], ignore_index=True)
        st.rerun()

with col_genai:
    st.header("🤖 GenAI Co-Pilot")
    if st.button("⚡ Generate Daily Report"):
        st.success("Report Generated!")
        st.write("PPE Compliance: 94%")

st.caption("HKT IOC PoC")
