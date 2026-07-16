import streamlit as st
from database import init_db, get_alerts, get_alert_by_id, resolve_alert
from style import STYLE, render_sidebar

if not st.session_state.get("logged_in"):
    st.rerun()

init_db()
uid = st.session_state.user_id
st.markdown(STYLE, unsafe_allow_html=True)
render_sidebar(st, st.session_state.username)


st.markdown('<div class="cp-title">Alerts</div><div class="cp-subtitle">All fall detection alerts for your monitored persons</div>', unsafe_allow_html=True)

if "selected_alert_id" not in st.session_state:
    st.session_state.selected_alert_id = None

alerts = get_alerts(uid)

st.markdown('<div class="cp-panel">', unsafe_allow_html=True)
if not alerts:
    st.markdown('<div class="cp-alert-meta">No alerts yet.</div>', unsafe_allow_html=True)
for a in alerts:
    badge_class = "cp-badge-resolved" if a["resolved"] else ("cp-badge-high" if a["priority"] == "High" else "cp-badge-medium")
    badge_text = "Resolved" if a["resolved"] else f"{a['priority']} Priority"
    col1, col2 = st.columns([5, 1])
    with col1:
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
                <span class="cp-badge {badge_class}">{badge_text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        if st.button("Details", key=f"btn_{a['id']}"):
            st.session_state.selected_alert_id = a["id"]
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.selected_alert_id:
    detail = get_alert_by_id(st.session_state.selected_alert_id, uid)
    if detail:
        st.markdown(
            f"""
            <div class="cp-detail-card">
                <div class="cp-detail-title">Fall Detected</div>
                <div class="cp-alert-meta">{detail['timestamp']}</div>
                <div style="margin-top:1rem;">
                    <div class="cp-detail-row"><span class="cp-detail-label">Person</span><span class="cp-detail-value">{detail['person_name']}</span></div>
                    <div class="cp-detail-row"><span class="cp-detail-label">Location</span><span class="cp-detail-value">{detail['room']}</span></div>
                    <div class="cp-detail-row"><span class="cp-detail-label">Confidence</span><span class="cp-detail-value">{(detail['confidence'] or 0) * 100:.0f}%</span></div>
                    <div class="cp-detail-row"><span class="cp-detail-label">Priority</span><span class="cp-detail-value">{detail['priority']}</span></div>
                    <div class="cp-detail-row"><span class="cp-detail-label">Status</span><span class="cp-detail-value">{'Resolved' if detail['resolved'] else 'Unresolved'}</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        c1, c2 = st.columns(2)
        with c1:
            if not detail["resolved"]:
                if st.button("✓ Mark as Resolved"):
                    resolve_alert(detail["id"], detail["person_id"])
                    st.session_state.selected_alert_id = None
                    st.rerun()
        with c2:
            if st.button("Close"):
                st.session_state.selected_alert_id = None
                st.rerun()