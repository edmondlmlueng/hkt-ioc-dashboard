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
    
    /* Equipment Status Style Blocks inside Sidebar */
    .status-card { background-color: #111A2E; padding: 10px 12px; border-radius: 6px; border: 1px solid #1E2D4A; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .badge-online { background-color: rgba(0, 224, 150, 0.15); color: #00E096; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; border: 1px solid #00E096; }
    .badge-warning { background-color: rgba(255, 170, 0, 0.15); color: #FFAA00; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; border: 1px solid #FFAA00; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ HKT Smart Site Integrated Operations Centre (IOC)")
st.subheader("Real-Time Safety Compliance & Analytics Terminal")
st.markdown("---")

# Sidebar Layout with Telemetry & Infrastructure Blocks
with st.sidebar:
    st.header("Site Telemetry")
    st.metric("Active Cameras", "4 / 4")
    st.metric("Alert Status", "ALARM ACTIVE", "-2 Violations")
    st.info("Location: Kowloon District, HK")
    
    st.markdown("---")
    
    # Infrastructure & Equipment Status Section
    st.header("🖥️ Device Infrastructure")
    st.markdown("""
    <div class="status-card">
        <div><strong>☁️ Drive Sync Server</strong><br><small style='color:#8A99AD;'>site_events.txt</small></div>
        <span class="badge-online">CONNECTED</span>
    </div>
    <div class="status-card">
        <div><strong>📸 Site Cam-01</strong><br><small style='color:#8A99AD;'>Area A Excavation</small></div>
        <span class="badge-online">ONLINE</span>
    </div>
    <div class="status-card">
        <div><strong>📸 Site Cam-02</strong><br><small style='color:#8A99AD;'>Zone B Scaffold</small></div>
        <span class="badge-warning">LAGGING</span>
    </div>
    <div class="status-card">
        <div><strong>🖥️ HKT Compute Core</strong><br><small style='color:#8A99AD;'>Analytics Hub Node</small></div>
        <span class="badge-online">ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

# --- Automated Google Drive Text Parser Logic ---
def fetch_and_parse_site_events():
    try:
        results = service.files().list(
            q=f"'{FOLDER_ID}' in parents and name = 'site_events.txt' and trashed=false",
            fields="files(id, name)"
        ).execute()
        
        items = results.get('files', [])
        if not items:
            return None
            
        file_id = items[0]['id']
        
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            
        file_stream.seek(0)
        raw_text = file_stream.read().decode('utf-8')
        
        parsed_logs = []
        lines = raw_text.split('\n')
        
        for line in lines:
            if "|" in line:
                tokens = line.split("|")
                log_entry = {}
                for token in tokens:
                    if ":" in token:
                        key, val = token.split(":", 1)
                        k_clean = key.strip().upper()
                        v_clean = val.strip()
                        
                        if "TIMESTAMP" in k_clean: log_entry["Timestamp"] = v_clean
                        elif "ZONE" in k_clean: log_entry["Zone"] = v_clean
                        elif "EVENT" in k_clean: log_entry["Violation"] = v_clean
                        elif "CONFIDENCE" in k_clean: log_entry["Confidence"] = v_clean
                
                if "Violation" in log_entry:
                    random.seed(hash(log_entry.get("Zone", "Default")))
                    log_entry["X"] = random.randint(10, 90)
                    log_entry["Y"] = random.randint(10, 90)
                    parsed_logs.append(log_entry)
                    
        if parsed_logs:
            return pd.DataFrame(parsed_logs)
    except Exception as parse_error:
        st.sidebar.error(f"Failed to scan site_events.txt: {str(parse_error)}")
    return None

parsed_df = fetch_and_parse_site_events()

if parsed_df is not None:
    st.session_state.event_logs = parsed_df
elif "event_logs" not in st.session_state:
    st.session_state.event_logs = pd.DataFrame([
        {"Timestamp": "2026-06-25 09:15", "Zone": "Area A", "Violation": "Missing Hard Hat", "Confidence": "88%", "X": 45, "Y": 65},
    ])

# 3-Column Layout Grid
col_video, col_logs, col_genai = st.columns([4, 3, 4])

# Video Section
with col_video:
    with st.container(border=True):
        st.subheader("📹 CCTV Live Feed")
        secure_nhk_stream = "https://fastv.jp"
        st.video(secure_nhk_stream, format="video/mp4", autoplay=True, muted=True, loop=True)
        st.caption("🔴 LIVE FEED CHANNEL: CONNECTED (Kowloon Hub Cam-01)")

# Google Drive Alerts + Restored Event Log
with col_logs:
    with st.container(border=True):
        st.subheader("🚨 Latest Alerts from Google Drive")
        if st.button("🔄 Refresh from Google Drive"):
            st.rerun()
        
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
    # --- Part 1: Spatial Alert Heatmap Card ---
    with st.container(border=True):
        st.subheader("🗺️ Zone Violation Spatial Heatmap")
        
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

    # --- Part 2: Event Analytics Table ---
    with st.container(border=True):
        st.subheader("📊 Event Analytics Table")
        view_df = st.session_state.event_logs[["Timestamp", "Zone", "Violation", "Confidence"]]
        st.dataframe(view_df, use_container_width=True, hide_index=True, height=150)

    # --- Part 3: GenAI Copilot Workspace Card ---
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
