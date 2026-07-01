import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HKT Smart Site IOC", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0B111E; }
    .stButton>button { background-color: #00C2FF; color: white; }
    .report-box { background-color: #161F30; padding: 20px; border-radius: 8px; border-left: 5px solid #00C2FF; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ HKT Smart Site Integrated Operations Centre (IOC)")
st.subheader("Real-Time Safety Compliance & Analytics Terminal")
st.markdown("---")

if "event_logs" not in st.session_state:
    st.session_state.event_logs = pd.DataFrame([
        {"Timestamp": "2026-06-25 09:15", "Zone": "Area A", "Violation": "Missing Hard Hat", "Confidence": "88%"},
    ])

col_video, col_logs, col_genai = st.columns([4, 3, 4])

with col_video:
    st.header("📹 CCTV Live Feed")
    st.info("Demo Mode - Big Buck Bunny Test Stream")
    st.image("https://picsum.photos/id/1015/800/450", use_container_width=True, caption="Live Feed (Demo)")

with col_logs:
    st.header("📋 Live Incident Log")
    st.dataframe(st.session_state.event_logs, use_container_width=True, hide_index=True)
    if st.button("Simulate New Alert"):
        new = {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "Zone": "Zone B", "Violation": "Intrusion", "Confidence": "95%"}
        st.session_state.event_logs = pd.concat([st.session_state.event_logs, pd.DataFrame([new])], ignore_index=True)
        st.rerun()

with col_genai:
    st.header("🤖 GenAI Safety Co-Pilot")
    if st.button("⚡ COMPILE DAILY SHIFT REPORT"):
        st.markdown("### 📄 Daily Safety Report")
        st.markdown("<div class='report-box'>PPE Compliance: 94%. No major violations. Recommendation: Monitor Zone B.</div>", unsafe_allow_html=True)

st.caption("HKT IOC PoC - Cloud Version")