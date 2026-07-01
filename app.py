import streamlit as st
import pandas as pd
from datetime import datetime
import os

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

# Sidebar
with st.sidebar:
    st.header("📁 Shared Alert Folder")
    st.write("Google Drive Folder Connected")
    st.caption("https://drive.google.com/drive/folders/1STpOEXxtgMvb-Ova_UrMF9E6CNLJCoAR")

# Session State
if "event_logs" not in st.session_state:
    st.session_state.event_logs = pd.DataFrame([
        {"Timestamp": "2026-06-25 09:15", "Zone": "Area A", "Violation": "Missing Hard Hat", "Confidence": "88%"},
    ])

col_video, col_logs, col_genai = st.columns([4, 3, 4])

# Video Section (Demo)
with col_video:
    st.header("📹 CCTV Live Feed")
    st.info("Demo Mode - Big Buck Bunny Test Stream")
    st.image("https://picsum.photos/id/1015/800/450", use_container_width=True, caption="Live Feed (Demo)")

# Alerts from Google Drive
with col_logs:
    st.header("🚨 Latest Alerts from Edge Team")
    refresh = st.button("🔄 Refresh from Google Drive")

    if refresh:
        st.info("Scanning Google Drive folder... (Demo Mode)")
        # In real version, we would list files from your folder
        st.success("New alert received from Edge team!")
        
        new_alert = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Zone": "Zone B",
            "Violation": "Missing PPE",
            "Confidence": "91%"
        }
        st.session_state.event_logs = pd.concat([st.session_state.event_logs, pd.DataFrame([new_alert])], ignore_index=True)

    st.dataframe(st.session_state.event_logs, use_container_width=True, hide_index=True)

# GenAI
with col_genai:
    st.header("🤖 GenAI Safety Co-Pilot")
    if st.button("⚡ COMPILE DAILY SHIFT REPORT"):
        st.markdown("### 📄 Daily Safety Audit Report")
        st.markdown("""
        <div class='report-box'>
        New alerts from Google Drive processed.<br><br>
        PPE Compliance: 91%<br>
        Recommendation: Review Zone B photos.
        </div>
        """, unsafe_allow_html=True)

st.caption("HKT Smart Site IOC PoC • Connected to Google Drive")
