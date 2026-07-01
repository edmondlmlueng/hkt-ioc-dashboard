import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HKT Smart Site IOC", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0B111E; }
    .stButton>button { background-color: #00C2FF; color: white; border-radius: 5px; font-weight: bold; }
    .report-box { background-color: #161F30; padding: 20px; border-radius: 8px; border-left: 5px solid #00C2FF; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ HKT Smart Site Integrated Operations Centre (IOC)")
st.subheader("Real-Time Safety Compliance & Analytics Terminal")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Site Telemetry")
    st.metric("Active Cameras", "4 / 4")
    st.metric("Alert Status", "ALARM ACTIVE", "-2 Violations")
    st.info("Location: Kowloon District, HK")

# Session State
if "event_logs" not in st.session_state:
    st.session_state.event_logs = pd.DataFrame([
        {"Timestamp": "2026-06-25 09:15", "Zone": "Area A", "Violation": "Missing Hard Hat", "Confidence": "88%"},
        {"Timestamp": "2026-06-25 10:30", "Zone": "Zone B", "Violation": "Missing High-Vis Vest", "Confidence": "92%"},
    ])

col_video, col_logs, col_genai = st.columns([4, 3, 4])

# Video Section (RTSP Demo)
with col_video:
    st.header("📹 CCTV Live Feed")
    video_frame = st.empty()
    video_status = st.empty()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start Live Feed"):
            st.session_state.video_running = True
            video_status.success("✅ Live feed started (Demo)")
    with col2:
        if st.button("⏹️ Stop Live Feed"):
            st.session_state.video_running = False
            video_status.info("Feed stopped")

    if st.session_state.get("video_running", False):
        st.image("https://picsum.photos/id/1015/800/450", use_container_width=True, caption="Live CCTV Feed - North Gate (Demo)")
    else:
        st.image("https://picsum.photos/id/1015/800/450", use_container_width=True, caption="Click 'Start Live Feed' to activate")

# Logs Section
with col_logs:
    st.header("📋 Live Incident Log")
    st.dataframe(st.session_state.event_logs, use_container_width=True, hide_index=True)
    
    if st.button("Simulate New Alert"):
        new_alert = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Zone": "Material Storage",
            "Violation": "Intrusion Detected",
            "Confidence": "95%"
        }
        st.session_state.event_logs = pd.concat([st.session_state.event_logs, pd.DataFrame([new_alert])], ignore_index=True)
        st.rerun()

# GenAI Section
with col_genai:
    st.header("🤖 GenAI Safety Co-Pilot")
    st.write("Automate compliance workflows.")
    
    if st.button("⚡ COMPILE DAILY SHIFT REPORT"):
        st.info("📝 GenAI Report (Demo Mode)")
        st.markdown("### 📄 Daily Safety Audit Report")
        st.markdown("""
        <div class='report-box'>
        No major violations detected today.<br><br>
        PPE Compliance Rate: 94%<br>
        Top Risk Zone: Zone B Scaffold<br>
        Recommendation: Increase helmet checks in Area A.
        </div>
        """, unsafe_allow_html=True)

st.caption("HKT Smart Site IOC PoC • Cloud Version")
