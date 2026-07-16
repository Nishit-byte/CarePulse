import streamlit as st
from database import init_db, get_persons, get_person_by_id, get_alerts, get_devices, add_person, delete_person, clear_live_person
from style import STYLE, render_sidebar

if not st.session_state.get("logged_in"):
    st.rerun()

init_db()
uid = st.session_state.user_id
st.markdown(STYLE, unsafe_allow_html=True)
render_sidebar(st, st.session_state.username)


st.markdown('<div class="cp-title">Monitored Persons</div><div class="cp-subtitle">People currently under your CarePulse monitoring</div>', unsafe_allow_html=True)

if "selected_person_id" not in st.session_state:
    st.session_state.selected_person_id = None
if "show_add_person" not in st.session_state:
    st.session_state.show_add_person = False

devices = get_devices(uid)

top1, top2 = st.columns([4, 1])
with top2:
    if st.button("➕ Add Person", use_container_width=True):
        st.session_state.show_add_person = not st.session_state.show_add_person

if st.session_state.show_add_person:
    st.markdown('<div class="cp-panel"><div class="cp-panel-title">Add a New Person</div>', unsafe_allow_html=True)
    with st.form("add_person_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=65)
        room = st.text_input("Room")
        device_options = {f"{d['room']} Sensor (id {d['id']})": d["id"] for d in devices}
        device_options["No device yet"] = None
        device_choice = st.selectbox("Assign Device", options=list(device_options.keys()))
        is_live_check = st.checkbox("This is the person monitored by my webcam (live detection)")
        submitted = st.form_submit_button("Add Person")
        if submitted:
            if not name or not room:
                st.error("Name and room are required.")
            else:
                if is_live_check:
                    clear_live_person(uid)
                add_person(uid, name, int(age), room, device_options[device_choice], is_live=1 if is_live_check else 0)
                st.session_state.show_add_person = False
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

persons = get_persons(uid)

left, right = st.columns([1, 1.3])

with left:
    st.markdown('<div class="cp-panel"><div class="cp-panel-title">All Persons</div>', unsafe_allow_html=True)
    if not persons:
        st.markdown('<div class="cp-alert-meta">No one added yet. Click "Add Person" above.</div>', unsafe_allow_html=True)
    for p in persons:
        badge_class = "cp-badge-high" if p["status"] == "Fall Detected" else "cp-badge-good"
        live_tag = '<span class="cp-live-tag">LIVE</span>' if p["is_live"] else ""
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                f"""
                <div class="cp-person-row">
                    <div>
                        <div class="cp-person-name">{p['name']}{live_tag}</div>
                        <div class="cp-person-room">Room: {p['room']}</div>
                    </div>
                    <span class="cp-badge {badge_class}">{p['status']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            if st.button("View", key=f"view_{p['id']}"):
                st.session_state.selected_person_id = p["id"]
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    if st.session_state.selected_person_id:
        p = get_person_by_id(st.session_state.selected_person_id, uid)
        if p:
            person_alerts = [a for a in get_alerts(uid) if a["person_id"] == p["id"]]
            last_activity = person_alerts[0]["timestamp"] if person_alerts else "No activity yet"
            initials = "".join([n[0] for n in p["name"].split()[:2]]).upper()
            st.markdown(
                f"""
                <div class="cp-panel">
                    <div class="cp-profile-avatar">{initials}</div>
                    <div class="cp-profile-name">{p['name']}</div>
                    <div class="cp-profile-sub">Age: {p['age'] or 'Not set'}</div>
                    <div class="cp-detail-row"><span class="cp-detail-label">Location</span><span class="cp-detail-value">{p['room']}</span></div>
                    <div class="cp-detail-row"><span class="cp-detail-label">Status</span><span class="cp-detail-value">{p['status']}</span></div>
                    <div class="cp-detail-row"><span class="cp-detail-label">Total Falls Logged</span><span class="cp-detail-value">{len(person_alerts)}</span></div>
                    <div class="cp-detail-row"><span class="cp-detail-label">Last Activity</span><span class="cp-detail-value">{last_activity}</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if p["is_live"]:
                st.markdown('<div class="cp-alert-meta">This is your live-monitored account and cannot be deleted.</div>', unsafe_allow_html=True)
            else:
                if st.button("🗑 Delete Person", use_container_width=True):
                    delete_person(p["id"], uid)
                    st.session_state.selected_person_id = None
                    st.rerun()
    else:
        st.markdown('<div class="cp-panel"><div class="cp-subtitle">Select a person to view their profile.</div></div>', unsafe_allow_html=True)