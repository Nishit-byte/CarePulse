import streamlit as st
import cv2
import time
from database import init_db, get_devices, get_persons, get_live_person, get_alerts, add_device, delete_device
from style import STYLE, render_sidebar

if not st.session_state.get("logged_in"):
    st.rerun()

init_db()
uid = st.session_state.user_id
st.markdown(STYLE, unsafe_allow_html=True)
render_sidebar(st, st.session_state.username)


st.markdown('<div class="cp-title">Devices</div><div class="cp-subtitle">Cameras connected to your CarePulse network</div>', unsafe_allow_html=True)

if "adding_device_index" not in st.session_state:
    st.session_state.adding_device_index = None

@st.cache_data(show_spinner=False)
def detect_cameras(max_index=4):
    available = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available.append(i)
            cap.release()
    return available

st.markdown('<div class="cp-panel"><div class="cp-panel-title">Available Cameras on This Laptop</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([3, 1])
with col_b:
    if st.button("🔍 Scan", use_container_width=True):
        st.cache_data.clear()

with st.spinner("Scanning for connected cameras..."):
    cameras = detect_cameras()

registered_devices = get_devices(uid)

if not cameras:
    st.markdown('<div class="cp-alert-meta">No cameras detected. Make sure your webcam is not in use by another app.</div>', unsafe_allow_html=True)
else:
    for cam_index in cameras:
        label = "Built-in Webcam" if cam_index == 0 else f"External Camera {cam_index}"
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(
                f"""
                <div class="cp-device-card">
                    <div class="cp-device-left">
                        <div class="cp-device-icon">📷</div>
                        <div>
                            <div class="cp-device-name">{label}</div>
                            <div class="cp-device-meta">Camera Index {cam_index}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with c2:
            if st.button("➕ Add as Device", key=f"add_{cam_index}"):
                st.session_state.adding_device_index = cam_index
                st.rerun()

if st.session_state.adding_device_index is not None:
    st.markdown(
        f'<div class="cp-alert-meta" style="margin-top:0.8rem;">Registering camera index {st.session_state.adding_device_index} — give it a room name:</div>',
        unsafe_allow_html=True
    )
    with st.form("add_device_form"):
        room_name = st.text_input("Room Name", placeholder="e.g. Living Room, Bedroom, Kitchen")
        submitted = st.form_submit_button("Register Device")
        if submitted:
            if not room_name:
                st.error("Room name is required.")
            else:
                add_device(uid, room_name, "online")
                st.session_state.adding_device_index = None
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel"><div class="cp-panel-title">Registered Monitoring Devices</div>', unsafe_allow_html=True)
persons = get_persons(uid)
if not registered_devices:
    st.markdown('<div class="cp-alert-meta">No devices registered yet. Add one from the cameras above.</div>', unsafe_allow_html=True)
for d in registered_devices:
    assigned = next((p["name"] for p in persons if p["device_id"] == d["id"]), "Unassigned")
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown(
            f"""
            <div class="cp-device-card">
                <div class="cp-device-left">
                    <div class="cp-device-icon">📡</div>
                    <div>
                        <div class="cp-device-name">{d['room']} Sensor</div>
                        <div class="cp-device-meta">Monitoring: {assigned}</div>
                    </div>
                </div>
                <span class="cp-online-badge">● Online</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        if st.button("🗑 Delete", key=f"del_dev_{d['id']}"):
            delete_device(d["id"], uid)
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel"><div class="cp-panel-title">Live Monitoring Status</div>', unsafe_allow_html=True)
live_person = get_live_person(user_id=uid)
if live_person is None:
    st.markdown('<div class="cp-alert-meta">No live-monitored person configured for your account.</div>', unsafe_allow_html=True)
else:
    recent_alerts = get_alerts(uid, limit=1)
    is_falling = live_person["status"] == "Fall Detected"
    if is_falling:
        st.markdown(
            '<span class="cp-badge cp-badge-high" style="font-size:1rem; padding:0.6rem 1.2rem;">⚠ Fall Detected — Alert Sent</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="cp-badge cp-badge-good" style="font-size:1rem; padding:0.6rem 1.2rem;">✓ All Normal</span>',
            unsafe_allow_html=True
        )
    if recent_alerts:
        st.markdown(f'<div class="cp-alert-meta" style="margin-top:0.8rem;">Last alert: {recent_alerts[0]["timestamp"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="cp-alert-meta" style="margin-top:0.4rem;">Run <code>python fall_detection_ml.py {st.session_state.username}</code> in a terminal to start live detection for your account.</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)