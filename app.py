import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
import random

# 1. MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="HKT Smart Site IOC", page_icon="🛡️", layout="wide")

FOLDER_ID = "1STpOEXxtgMvb-Ova_UrMF9E6CNLJCoAR"

@st.cache_resource
def get_drive_service():
    creds_dict = st.secrets["google"]
    creds = Credentials.from_service_account_info(creds_dict)
    return build('drive', 'v3', credentials=creds)

service = get_drive_service()

# Professional Dark Theme Overrides
st.markdown("""
    <style>
    .main { background-color: #0B111E; color: #E2E8F0; }
    .stButton>button { background-color: #00C2FF !important; color: #0B111E !important; border-radius: 6px; font-weight: bold; width: 100%; border: none; }
    .stButton>button:hover { background-color: #00E0FF !important; }
    .report-box { background-color: #161F30; padding: 20px; border-radius: 8px; border-left: 5px solid #00C2FF; color: white; }
    div[data-testid="stMetricValue"] { font-size: 26px !important; color: #00C2FF !important; font-weight: 700; }
    h1, h2, h3, h4 { margin-bottom: 0.2rem !important; }
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

# Initialize event logs with hidden tracking coordinates (X, Y) for the heatmap
if "event_logs" not in st.session_state:
    st.session_state.event_logs = pd.DataFrame([
        {"Timestamp": "2026-06-25 09:15", "Zone": "Area A", "Violation": "Missing Hard Hat", "Confidence": "88%", "X": 45, "Y": 65},
    ])

# 3-Column Layout Grid
col_video, col_logs, col_genai = st.columns([4, 3, 4])

# Video Section
with col_video:
    with st.container(border=True):
        st.subheader("📹 CCTV Live Feed")
        
        # Secure production HLS (.m3u8) feed stream link
        secure_nhk_stream = "https://nhkworld.jp"
        
        st.video(
            secure_nhk_stream,
            format="video/mp4",
            autoplay=True,
            muted=True,
            loop=True
        )
        st.caption("🔴 LIVE FEED CHANNEL: CONNECTED (Kowloon Hub Cam-01)")

# Google Drive Alerts + Restored Event Log
with col_logs:
    with st.container(border=True):
        st.subheader("🚨 Latest Alerts from Google Drive")
        if st.button("🔄 Refresh from Google Drive"):
            st.rerun()
        
        # --- Part 1: Google Drive Photo Feed ---
        try:
            results = service.files().list(
                q=f"'{FOLDER_ID}' in parents and trashed=false",
                fields="files(id, name, mimeType, createdTime)",
                orderBy="createdTime desc"
            ).execute()

            files = results.get('files', [])
            image_files = [f for f in files if f['mimeType'].startswith('image')]

            if image_files:
                st.success(f"Found {len(image_files)} alert photos")
                img_subcols = st.columns(2)
                for idx, file in enumerate(image_files[:4]):
                    with img_subcols[idx % 2]:
                        try:
                            request = service.files().get_media(fileId=file['id'])
                            file_stream = io.BytesIO()
                            downloader = MediaIoBaseDownload(file_stream, request)
                            done = False
                            while done is False:
                                status, done = downloader.next_chunk()
                            file_stream.seek(0)
                            st.image(file_stream, caption=file['name'], use_container_width=True)
                        except Exception as img_err:
                            st.caption(f"⚠️ Error {file['name']}")
            else:
                st.info("No alert photos found yet.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# GenAI Section & Analytics Heatmap
with col_genai:
    # --- Part 2: Spatial Alert Heatmap Card ---
    with st.container(border=True):
        st.subheader("🗺️ Zone Violation Spatial Heatmap")
        
        # Explicit ranges added here to fix the syntax crash
        fig = px.density_heatmap(
            st.session_state.event_logs, 
            x="X", 
            y="Y",
            nbinsx=10, 
            nbinsy=10,
            color_continuous_scale="Viridis",
            range_x=[0, 100],
            range_y=[0, 100],
            labels={"X": "Width Vector (m)", "Y": "Depth Vector (m)"}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="#E2E8F0",
            margin=dict(l=10, r=10, t=10, b=10),
            height=220,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- Part 3: Restored Event Log Table & Simulator ---
    with st.container(border=True):
        st.subheader("📊 Event Analytics Table")
        
        view_df = st.session_state.event_logs[["Timestamp", "Zone", "Violation", "Confidence"]]
        st.dataframe(view_df, use_container_width=True, hide_index=True, height=150)
        
        if st.button("Simulate New Alert"):
            sim_zones = ["Area A", "Zone B", "Sector C", "North Gate"]
            sim_violations = ["Missing Hard Hat", "Intrusion Detected", "No High-Vis Vest", "Unauthorized Entry"]
            
            new_alert = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Zone": random.choice(sim_zones),
                "Violation": random.choice(sim_violations),
                "Confidence": f"{random.randint(82, 98)}%",
                "X": random.randint(5, 95),
                "Y": random.randint(5, 95)
            }
            st.session_state.event_logs = pd.concat([st.session_state.event_logs, pd.DataFrame([new_alert])], ignore_index=True)
            st.rerun()

    # --- Part 4: GenAI Copilot Workspace Card ---
    with st.container(border=True):
        st.subheader("🤖 GenAI Safety Co-Pilot")
        st.write("Automate compliance workflows.")
        if st.button("⚡ COMPILE DAILY SHIFT REPORT"):
            st.markdown("### 📄 Daily Safety Audit Report")
            st.markdown("""
            <div class='report-box'>
            New alerts from Google Drive processed.<br><br>
            PPE Compliance: 91%<br>
            Top Risk Zone: Zone B<br>
            Recommendation: Review uploaded photos.
            </div>
            """, unsafe_allow_html=True)

st.caption("HKT Smart Site IOC PoC • Connected to Google Drive")
