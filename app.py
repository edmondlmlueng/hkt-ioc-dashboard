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

# --- [Omitted for brevity: Streamlit UI Styling] ---

st.title("🛡️ HKT Smart Site Integrated Operations Centre (IOC)")
st.subheader("Real-Time Safety Compliance & Analytics Terminal")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Site Telemetry")
    st.metric("Active Cameras", "4 / 4")
    st.metric("Alert Status", "ALARM ACTIVE", "-2 Violations")
    st.info("Location: Kowloon District, HK")

# Initialize base log storage structure
if "event_logs" not in st.session_state:
    st.session_state.event_logs = pd.DataFrame([
        {"Timestamp": "2026-06-25 09:15:00", "Zone": "Area A", "Violation": "Worker missing hard hat", "Confidence": "88%", "X": 45, "Y": 65},
    ])

# 3-Column Layout Grid
col_video, col_logs, col_genai = st.columns([4, 3, 4])

# Video Section
with col_video:
    with st.container(border=True):
        st.subheader("📹 CCTV Live Feed")
        st.video("https://fastv.jp", format="video/mp4", autoplay=True, muted=True, loop=True)
        st.caption("🔴 LIVE FEED: CONNECTED (Kowloon Hub)")

# Google Drive Alerts + Log Fetch Engine
with col_logs:
    with st.container(border=True):
        st.subheader("🚨 Latest Alerts from Google Drive")
        refresh_triggered = st.button("🔄 Refresh from Google Drive")
        
        # --- Part 1: Automated site_events.txt Cloud Parser Sync ---
        try:
            log_search = service.files().list(
                q=f"'{FOLDER_ID}' in parents and name = 'site_events.txt' and trashed=false",
                fields="files(id, name)"
            ).execute()
            
            target_log_files = log_search.get('files', [])
            
            if target_log_files:
                txt_file_id = target_log_files[0]['id']
                request_txt = service.files().get_media(fileId=txt_file_id)
                bytes_buffer = io.BytesIO()
                txt_downloader = MediaIoBaseDownload(bytes_buffer, request_txt)
                
                done = False
                while done is False:
                    _, done = txt_downloader.next_chunk()
                
                # Turn raw binary package back to structural readable strings
                bytes_buffer.seek(0)
                decoded_raw_text = bytes_buffer.read().decode('utf-8')
                
                # Extract items by line break parameters
                incoming_records = []
                for line in decoded_raw_text.split('\n'):
                    if "|" in line:
                        subsections = line.split("|")
                        parsed_item = {}
                        for chunk in subsections:
                            if ":" in chunk:
                                key, value = chunk.split(":", 1)
                                parsed_item[key.strip().capitalize()] = value.strip()
                        
                        # Add mock coords for demo
                        if "Violation" in parsed_item:
                            parsed_item["X"] = random.randint(10, 90)
                            parsed_item["Y"] = random.randint(10, 90)
                            incoming_records.append(parsed_item)
                
                if incoming_records and refresh_triggered:
                    st.session_state.event_logs = pd.DataFrame(incoming_records)
                    st.toast("Remote text telemetry logs synched up successfully!", icon="📝")
            else:
                st.caption("ℹ️ No remote 'site_events.txt' file found.")
        except Exception as txt_error:
            st.caption(f"⚠️ Text Log Processing Notice: {str(txt_error)}")

        # --- Part 2: Google Drive Photo Feed ---
        # ... (Image fetching logic remains same) ...

# GenAI Section & Analytics Heatmap
with col_genai:
    # --- Part 3: Supervisor Real-Time Urgent Flag Banner Engine ---
    for _, row in st.session_state.event_logs.iterrows():
        if any(w in str(row['Violation']).lower() for w in ["missing", "intrusion"]):
            st.error(f"🚨 **URGENT**: {row['Violation']} at {row['Zone']}")

    # --- Part 4: Spatial Alert Heatmap Card ---
    # ... (Plotly chart code) ...

    # --- Part 5: Event Log Table & Simulator ---
    # ... (Table and button code) ...

st.caption("HKT Smart Site IOC • Connected to Google Drive")
