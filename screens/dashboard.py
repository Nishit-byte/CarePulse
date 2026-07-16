import streamlit as st
import pandas as pd
from database import (
    init_db, get_persons, get_devices, get_alerts,
    get_active_alert_count, get_total_falls_this_month, get_fall_counts_by_day
)
from style import STYLE, render_sidebar

if not st.session_state.get("logged_in"):
    st.rerun()

init_db()
uid = st.session_state.user_id
st.markdown(STYLE, unsafe_allow_html=True)
render_sidebar(st, st.session_state.username)


persons = get_persons(uid)
devices = get_devices(uid)
alerts = get_alerts(uid, limit=5)
active_alerts = get_active_alert_count(uid)
falls_this_month = get_total_falls_this_month(uid)

st.markdown(
    """
    <div class="cp-title">Dashboard</div>
    <div class="cp-subtitle">Overview of your loved one's safety</div>
    """,
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)
stat_cards = [
    (c1, "#DCF3E4", "#22A06B", "👥", str(len(persons)), "Monitored Person", "All active"),
    (c2, "#FCE4E4", "#E5484D", "⚠", str(active_alerts), "Active Alerts", "Needs attention"),
    (c3, "#DCEAFB", "#2F6FE4", "✓", str(len(devices)), "Devices Online", "All connected"),
    (c4, "#EFE3FB", "#8B5CF6", "📈", str(falls_this_month), "Total Falls (This Month)", "View reports"),
]
for col, bg, fg, icon, value, label, sub in stat_cards:
    with col:
        st.markdown(
            f"""
            <div class="cp-stat-card">
                <div class="cp-stat-icon" style="background:{bg}; color:{fg};">{icon}</div>
                <div class="cp-stat-value">{value}</div>
                <div class="cp-stat-label">{label}</div>
                <div class="cp-stat-sub" style="color:{fg};">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

left, right = st.columns([1.15, 1])

with left:
    st.markdown('<div class="cp-panel"><div class="cp-panel-title">Recent Alerts</div>', unsafe_allow_html=True)
    if not alerts:
        st.markdown('<div class="cp-alert-meta">No alerts yet.</div>', unsafe_allow_html=True)
    for a in alerts[:3]:
        badge_class = "cp-badge-high" if a["priority"] == "High" else "cp-badge-medium"
        st.markdown(
            f"""
            <div class="cp-alert-row">
                <div class="cp-alert-left">
                    <div class="cp-alert-dot">⚠</div>
                    <div>
                        <div class="cp-alert-name">Fall Detected — {a['person_name']}</div>
                        <div class="cp-alert-meta">{a['timestamp']} · {a['room']}</div>
                    </div>
                </div>
                <span class="cp-badge {badge_class}">{a['priority']} Priority</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("screens/alerts.py", label="View all alerts →")

    st.markdown('<div class="cp-panel"><div class="cp-panel-title">Fall Activity (This Month)</div>', unsafe_allow_html=True)
    day_counts = get_fall_counts_by_day(uid)
    if day_counts:
        df = pd.DataFrame(day_counts, columns=["Day", "Falls"]).set_index("Day")
        st.line_chart(df, color="#2F6FE4", height=220)
    else:
        st.markdown('<div class="cp-alert-meta">No fall activity recorded yet.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="cp-panel"><div class="cp-panel-title">Monitored Person Status</div>', unsafe_allow_html=True)
    if not persons:
        st.markdown('<div class="cp-alert-meta">No one added yet. Go to Users to add someone.</div>', unsafe_allow_html=True)
    for p in persons:
        badge_class = "cp-badge-high" if p["status"] == "Fall Detected" else "cp-badge-good"
        status_label = p["status"] if p["status"] == "Fall Detected" else "All Good"
        st.markdown(
            f"""
            <div class="cp-person-row">
                <div>
                    <div class="cp-person-name">{p['name']}</div>
                    <div class="cp-person-room">Room: {p['room']}</div>
                </div>
                <span class="cp-badge {badge_class}">{status_label}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("screens/users.py", label="View all persons →")

    st.markdown('<div class="cp-panel"><div class="cp-panel-title">Devices Status</div>', unsafe_allow_html=True)
    if not devices:
        st.markdown('<div class="cp-alert-meta">No devices added yet.</div>', unsafe_allow_html=True)
    for d in devices:
        st.markdown(
            f"""
            <div class="cp-device-row">
                <div class="cp-device-name">{d['room']} Sensor</div>
                <span class="cp-online-dot">● Online</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    st.page_link("screens/devices.py", label="View all devices →")

if st.button("🔄 Refresh"):
    st.rerun()