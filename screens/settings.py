import streamlit as st
import os
from database import init_db, get_motionless_seconds, update_motionless_seconds
from style import STYLE, render_sidebar

if not st.session_state.get("logged_in"):
    st.rerun()

init_db()
uid = st.session_state.user_id
st.markdown(STYLE, unsafe_allow_html=True)
render_sidebar(st, st.session_state.username)


st.markdown('<div class="cp-title">Settings</div><div class="cp-subtitle">Manage your CarePulse preferences</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel cp-panel-narrow"><div class="cp-panel-title">Account</div>', unsafe_allow_html=True)
st.text_input("Username", value=st.session_state.username, disabled=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel cp-panel-narrow"><div class="cp-panel-title">Emergency Contact</div>', unsafe_allow_html=True)
current_number = os.getenv("TWILIO_WHATSAPP_TO", "").replace("whatsapp:", "")
new_number = st.text_input("WhatsApp Number (with country code)", value=current_number)
st.markdown('<div class="cp-alert-meta">To change this permanently, update TWILIO_WHATSAPP_TO in your .env file and restart the app.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel cp-panel-narrow"><div class="cp-panel-title">Detection Sensitivity</div>', unsafe_allow_html=True)
current_window = get_motionless_seconds(uid)
new_window = st.slider(
    "Motionless confirmation window (seconds)",
    min_value=3, max_value=20, value=current_window,
    help="How long a person must stay motionless after a detected fall before an alert is sent."
)
if new_window != current_window:
    update_motionless_seconds(uid, new_window)
    st.toast(f"Sensitivity updated — alerts now fire after {new_window}s of no movement.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel cp-panel-narrow"><div class="cp-panel-title">Notifications</div>', unsafe_allow_html=True)
st.checkbox("WhatsApp alerts enabled", value=True, disabled=True)
st.checkbox("Email alerts enabled", value=False, disabled=True)
st.markdown('</div>', unsafe_allow_html=True)