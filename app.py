import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime

# ================== CONFIG ==================
FOLDER_ID = "1STpOEXxtgMvb-Ova_UrMF9E6CNLJCoAR"   # Your Google Drive Folder ID

# ================== Google Drive Setup using st.secrets ==================
@st.cache_resource
def get_drive_service():
    creds_dict = st.secrets["google"]
    creds = Credentials.from_service_account_info(creds_dict)
    return build('drive', 'v3', credentials=creds)

service = get_drive_service()

# ================== Streamlit App ==================
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
    st.header("📁 Shared Alert Folder")
    st.success("✅ Connected to Google Drive")
    st.caption("Folder ID: " + FOLDER_ID[:20] + "...")

# Layout
col_video, col_logs, col_genai = st.columns([4, 3, 4])

# Video Section
with col_video:
    st.header("📹 CCTV Live Feed")
    st.info
