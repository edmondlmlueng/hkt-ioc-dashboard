import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime

FOLDER_ID = "1STpOEXxtgMvb-Ova_UrMF9E6CNLJCoAR"

@st.cache_resource
def get_drive_service():
    creds_dict = st.secrets["google"]
    creds = Credentials.from_service_account_info(creds_dict)
    return build('drive', 'v3', credentials=creds)

service = get_drive_service()

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

col_video, col_logs, col_genai = st.columns([4, 3, 4])

# Video Section
with col_video:
    st.header("📹 CCTV Live Feed")
    st.info("Demo Mode - Big Buck Bunny Test Stream")
    st.image("https://picsum.photos/id/1015/800/450", use_container_width=True, caption="Live Feed (Demo)")

# Google Drive Alerts
with col_logs:
    st.header("🚨 Latest Alerts from Edge Team")
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
            for file in image_files[:8]:
                st.image(f"https://drive.google.com/uc?export=view&id={file['id']}", 
                        caption=file['name'], use_container_width=True)
        else:
            st.info("No alert photos found yet.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# GenAI Section
with col_genai:
    st.header("🤖 GenAI Safety Co-Pilot")
    st.write("Automate daily compliance workflows.")
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
