import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="HKT IOC", layout="wide")

st.title("🛡️ HKT Smart Site IOC")
st.subheader("Real-Time Safety Dashboard")

st.success("Dashboard is running")

col1, col2 = st.columns(2)

with col1:
    st.header("📹 CCTV Live Feed")
    st.image("https://picsum.photos/id/1015/800/450", use_container_width=True, caption="Live Feed (Demo)")

with col2:
    st.header("🚨 Alerts")
    if st.button("Simulate Alert"):
        st.success("New alert received!")

st.caption("Simple PoC Version")
