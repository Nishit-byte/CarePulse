import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
    df = pd.DataFrame(day_counts, columns=["Day", "Falls"])
    df["Day"] = pd.to_datetime(df["Day"])

    fig, ax = plt.subplots(figsize=(10, 3.2), dpi=150)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ax.plot(
        df["Day"], df["Falls"],
        color="#2F6FE4", linewidth=2.5, marker="o",
        markersize=6, markerfacecolor="#2F6FE4",
        markeredgecolor="#FFFFFF", markeredgewidth=1.5,
        zorder=3
    )
    ax.fill_between(df["Day"], df["Falls"], color="#2F6FE4", alpha=0.12, zorder=2)

    max_falls = int(df["Falls"].max())
    ax.set_ylim(0, max_falls + 1)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.set_xticks(df["Day"])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    span = (df["Day"].max() - df["Day"].min())
    pad = span * 0.1 if span.days > 0 else pd.Timedelta(days=1)
    ax.set_xlim(df["Day"].min() - pad, df["Day"].max() + pad)
    fig.autofmt_xdate(rotation=0, ha="center")

    ax.grid(axis="y", color="#E7EBF3", linewidth=0.8, zorder=1)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#D8DEEA")
    ax.tick_params(colors="#6B7280", labelsize=9)
    ax.set_ylabel("Falls", color="#6B7280", fontsize=9)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
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