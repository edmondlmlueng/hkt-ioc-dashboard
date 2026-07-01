import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HKT IOC", layout="wide")

st.title("🛡️ HKT Smart Site Integrated Operations Centre (IOC)")
st.subheader("Real-Time Safety Compliance & Analytics Terminal")

st.success("✅ Dashboard is running!")

col1, col2, col3 = st.columns([4, 3, 3])

with col1:
    st.header("📹 CCTV Live Feed")
    st.image("https://picsum.photos/id/1015/800/450", use_container_width=True, caption="North Gate - Live (Demo)")

with col2:
    st.header("🚨 Latest Alerts")
    if "logs" not in st.session_state:
        st.session_state.logs = pd.DataFrame([
            {"Time": "09:15", "Zone": "Area A", "Event": "Missing Hard Hat"},
            {"Time": "10:30", "Zone": "Zone B", "Event": "Missing Vest"},
        ])
    st.dataframe(st.session_state.logs, use_container_width=True)
    if st.button("Simulate New Alert"):
        new = {"Time": datetime.now().strftime("%H:%M"), "Zone": "Zone B", "Event": "PPE Violation"}
        st.session_state.logs = pd.concat([st.session_state.logs, pd.DataFrame([new])], ignore_index=True)
        st.rerun()

with col3:
    st.header("🤖 GenAI Co-Pilot")
    if st.button("⚡ Generate Daily Report"):
        st.markdown("### 📄 Daily Report")
        st.success("PPE Compliance: 94%")
        st.write("Recommendation: Check Zone B")

st.caption("HKT IOC PoC - Simple Version")
