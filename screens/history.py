import streamlit as st
import pandas as pd
from database import init_db, get_alerts, get_fall_counts_by_day
from style import STYLE, render_sidebar

if not st.session_state.get("logged_in"):
    st.rerun()

init_db()
uid = st.session_state.user_id
st.markdown(STYLE, unsafe_allow_html=True)
render_sidebar(st, st.session_state.username)


st.markdown('<div class="cp-title">History</div><div class="cp-subtitle">Full fall detection timeline</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel"><div class="cp-panel-title">Fall Activity Over Time</div>', unsafe_allow_html=True)
day_counts = get_fall_counts_by_day(uid)
if day_counts:
    df = pd.DataFrame(day_counts, columns=["Day", "Falls"]).set_index("Day")
    st.line_chart(df, color="#2F6FE4", height=260)
else:
    st.markdown('<div class="cp-alert-meta">No fall activity recorded yet.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="cp-panel"><div class="cp-panel-title">All Events</div>', unsafe_allow_html=True)
alerts = get_alerts(uid)
current_day = None
if not alerts:
    st.markdown('<div class="cp-alert-meta">No events yet.</div>', unsafe_allow_html=True)
for a in alerts:
    day = a["timestamp"].split(" ")[0]
    if day != current_day:
        st.markdown(f'<div class="cp-day-label">{day}</div>', unsafe_allow_html=True)
        current_day = day
    badge_class = "cp-badge-resolved" if a["resolved"] else "cp-badge-unresolved"
    badge_text = "Resolved" if a["resolved"] else "Unresolved"
    time_part = a["timestamp"].split(" ")[1] if " " in a["timestamp"] else ""
    st.markdown(
        f"""
        <div class="cp-alert-row">
            <div class="cp-alert-left">
                <div class="cp-alert-dot">⚠</div>
                <div>
                    <div class="cp-alert-name">Fall Detected — {a['person_name']}</div>
                    <div class="cp-alert-meta">{time_part} · {a['room']}</div>
                </div>
            </div>
            <span class="cp-badge {badge_class}">{badge_text}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)