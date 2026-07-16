import streamlit as st
import pandas as pd
from database import init_db, get_alerts, get_persons, get_fall_counts_by_day
from style import STYLE, render_sidebar

if not st.session_state.get("logged_in"):
    st.rerun()

init_db()
uid = st.session_state.user_id
st.markdown(STYLE, unsafe_allow_html=True)
render_sidebar(st, st.session_state.username)


st.markdown('<div class="cp-title">Reports</div><div class="cp-subtitle">Summary insights across your monitored persons</div>', unsafe_allow_html=True)

alerts = get_alerts(uid)
persons = get_persons(uid)

total_falls = len(alerts)
resolved = len([a for a in alerts if a["resolved"]])
avg_confidence = sum([(a["confidence"] or 0) for a in alerts]) / total_falls if total_falls else 0

c1, c2, c3 = st.columns(3)
report_stats = [
    (c1, "#DCEAFB", "#2F6FE4", "📊", str(total_falls), "Total Falls Logged"),
    (c2, "#DCF3E4", "#22A06B", "✓", str(resolved), "Resolved Incidents"),
    (c3, "#EFE3FB", "#8B5CF6", "🎯", f"{avg_confidence * 100:.0f}%", "Avg. Detection Confidence"),
]
for col, bg, fg, icon, value, label in report_stats:
    with col:
        st.markdown(
            f"""
            <div class="cp-stat-card">
                <div class="cp-stat-icon" style="background:{bg}; color:{fg};">{icon}</div>
                <div class="cp-stat-value">{value}</div>
                <div class="cp-stat-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.write("")

st.markdown('<div class="cp-panel"><div class="cp-panel-title">Falls by Person</div>', unsafe_allow_html=True)
if not persons:
    st.markdown('<div class="cp-alert-meta">No one added yet.</div>', unsafe_allow_html=True)
for p in persons:
    count = len([a for a in alerts if a["person_id"] == p["id"]])
    st.markdown(
        f"""
        <div class="cp-person-row">
            <div class="cp-person-name">{p['name']}</div>
            <div class="cp-person-room">{count} fall(s) logged</div>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel"><div class="cp-panel-title">Fall Trend</div>', unsafe_allow_html=True)
day_counts = get_fall_counts_by_day(uid)
if day_counts:
    df = pd.DataFrame(day_counts, columns=["Day", "Falls"]).set_index("Day")
    st.bar_chart(df, color="#2F6FE4", height=240)
else:
    st.markdown('<div class="cp-alert-meta">No data yet.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)