STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, header, footer { visibility: hidden; }
.stApp { background: #F7F9FC; }
.block-container { padding-top: 1.8rem; padding-bottom: 2.5rem; max-width: 1180px; }

section[data-testid="stSidebar"] {
    background: #161D34;
}
section[data-testid="stSidebar"] * {
    color: #C6CBE0 !important;
}
section[data-testid="stSidebar"] a {
    border-radius: 10px;
}
section[data-testid="stSidebar"] [aria-current="page"] {
    background: #232B4D;
    color: #FFFFFF !important;
}
section[data-testid="stSidebar"] [aria-current="page"] * {
    color: #FFFFFF !important;
}

.cp-brand {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.4rem 0.2rem 1.2rem 0.2rem;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid #2A3357;
}
.cp-brand-icon {
    width: 38px; height: 38px; border-radius: 11px;
    background: #2F6FE4; display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.cp-brand-name { font-weight: 800; font-size: 1.05rem; color: #FFFFFF; line-height: 1.1; }
.cp-brand-sub { font-size: 0.72rem; color: #8891B5; font-weight: 600; }

.cp-title { font-weight: 800; font-size: 1.9rem; color: #1A2135; margin: 0; }
.cp-subtitle { font-weight: 600; color: #8891A8; font-size: 0.9rem; margin-top: 0.15rem; margin-bottom: 1.4rem; }

.cp-stat-card {
    background: #FFFFFF; border-radius: 18px; padding: 1.3rem 1.3rem 1.1rem 1.3rem;
    box-shadow: 0 2px 10px rgba(20, 30, 60, 0.05); border: 1px solid #EEF1F8; height: 100%;
}
.cp-stat-icon {
    width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center;
    justify-content: center; font-size: 1.2rem; margin-bottom: 0.8rem;
}
.cp-stat-value { font-weight: 800; font-size: 1.8rem; color: #1A2135; line-height: 1; }
.cp-stat-label { font-weight: 700; font-size: 0.82rem; color: #1A2135; margin-top: 0.35rem; }
.cp-stat-sub { font-weight: 600; font-size: 0.76rem; margin-top: 0.15rem; }

.cp-panel {
    background: #FFFFFF; border-radius: 18px; padding: 1.4rem 1.5rem;
    box-shadow: 0 2px 10px rgba(20, 30, 60, 0.05); border: 1px solid #EEF1F8; margin-bottom: 1.2rem;
}
.cp-panel-title { font-weight: 700; font-size: 1.05rem; color: #1A2135; margin-bottom: 0.9rem; }

.cp-alert-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.75rem 0; border-bottom: 1px solid #F1F3F9;
}
.cp-alert-row:last-child { border-bottom: none; }
.cp-alert-left { display: flex; align-items: center; gap: 0.7rem; }
.cp-alert-dot {
    width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center;
    justify-content: center; background: #FCE4E4; color: #E5484D; font-size: 1.05rem;
}
.cp-alert-name { font-weight: 700; color: #1A2135; font-size: 0.92rem; }
.cp-alert-meta { font-weight: 500; color: #96A0B5; font-size: 0.78rem; }

.cp-badge { font-weight: 700; font-size: 0.72rem; padding: 0.25rem 0.7rem; border-radius: 999px; }
.cp-badge-high { background: #FCE4E4; color: #E5484D; }
.cp-badge-medium { background: #FDF0DC; color: #D08A1E; }
.cp-badge-good { background: #DCF3E4; color: #22A06B; }
.cp-badge-resolved { background: #DCF3E4; color: #22A06B; }
.cp-badge-unresolved { background: #FCE4E4; color: #E5484D; }

.cp-person-row { display: flex; align-items: center; justify-content: space-between; padding: 0.7rem 0; border-bottom: 1px solid #F1F3F9; }
.cp-person-row:last-child { border-bottom: none; }
.cp-person-name { font-weight: 700; color: #1A2135; font-size: 0.92rem; }
.cp-person-room { font-weight: 500; color: #96A0B5; font-size: 0.78rem; }
.cp-live-tag { background: #2F6FE4; color: #FFFFFF; font-size: 0.64rem; font-weight: 800; padding: 0.15rem 0.5rem; border-radius: 999px; margin-left: 0.5rem; }

.cp-device-row { display: flex; align-items: center; justify-content: space-between; padding: 0.65rem 0; border-bottom: 1px solid #F1F3F9; }
.cp-device-row:last-child { border-bottom: none; }
.cp-device-name { font-weight: 700; color: #1A2135; font-size: 0.9rem; }
.cp-online-dot { color: #22A06B; font-weight: 700; font-size: 0.78rem; }

.cp-device-card {
    background: #FFFFFF; border-radius: 18px; padding: 1.3rem 1.4rem;
    box-shadow: 0 2px 10px rgba(20, 30, 60, 0.05); border: 1px solid #EEF1F8;
    margin-bottom: 0.9rem; display: flex; align-items: center; justify-content: space-between;
}
.cp-device-left { display: flex; align-items: center; gap: 1rem; }
.cp-device-icon { width: 44px; height: 44px; border-radius: 12px; background: #DCF3E4; color: #22A06B; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
.cp-device-meta { font-weight: 500; color: #96A0B5; font-size: 0.8rem; }
.cp-online-badge { background: #DCF3E4; color: #22A06B; font-weight: 700; font-size: 0.76rem; padding: 0.35rem 0.9rem; border-radius: 999px; }

.cp-detail-card { background: #FDF3F3; border-radius: 18px; padding: 1.6rem; margin-top: 1rem; border: 1px solid #F9DCDC; }
.cp-detail-title { font-weight: 800; font-size: 1.35rem; color: #C0392B; margin-bottom: 0.2rem; }
.cp-detail-row { display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #F5DEDE; font-weight: 600; }
.cp-detail-row:last-child { border-bottom: none; }
.cp-detail-label { color: #96A0B5; font-size: 0.85rem; }
.cp-detail-value { color: #1A2135; font-size: 0.9rem; }

.cp-profile-avatar { width: 62px; height: 62px; border-radius: 50%; background: #E9EFFC; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.5rem; color: #2F6FE4; margin-bottom: 0.8rem; }
.cp-profile-name { font-weight: 800; font-size: 1.25rem; color: #1A2135; }
.cp-profile-sub { font-weight: 500; color: #96A0B5; font-size: 0.85rem; margin-bottom: 1.2rem; }

.cp-day-label { font-weight: 800; color: #96A0B5; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.04em; margin: 1rem 0 0.4rem 0; }

.stButton button {
    border-radius: 10px !important;
    font-weight: 700 !important;
    border: 1px solid #E4E8F2 !important;
}

.stTextInput input, .stTextArea textarea, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
    color: #1A2135 !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E4E8F2 !important;
    border-radius: 10px !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #96A0B5 !important;
}
.stTextInput label, .stTextArea label, .stNumberInput label, .stSelectbox label, .stSlider label, .stCheckbox label {
    color: #1A2135 !important;
    font-weight: 600 !important;
}
div[data-baseweb="select"] * {
    color: #1A2135 !important;
}
</style>
"""

def render_sidebar_brand(st):
    st.sidebar.markdown(
        """
        <div class="cp-brand">
            <div class="cp-brand-icon">🛡️</div>
            <div>
                <div class="cp-brand-name">CarePulse</div>
                <div class="cp-brand-sub">Fall Detection System</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_sidebar(st, username):
    st.sidebar.markdown(
        """
        <div class="cp-brand">
            <div class="cp-brand-icon">🛡️</div>
            <div>
                <div class="cp-brand-name">CarePulse</div>
                <div class="cp-brand-sub">Fall Detection System</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.page_link("screens/dashboard.py", label="Dashboard", icon="🏠")
    st.sidebar.page_link("screens/alerts.py", label="Alerts", icon="🔔")
    st.sidebar.page_link("screens/history.py", label="History", icon="🕐")
    st.sidebar.page_link("screens/users.py", label="Users", icon="👥")
    st.sidebar.page_link("screens/devices.py", label="Devices", icon="📷")
    st.sidebar.page_link("screens/reports.py", label="Reports", icon="📊")
    st.sidebar.page_link("screens/settings.py", label="Settings", icon="⚙️")

    st.sidebar.write("")
    st.sidebar.markdown(f'<div class="cp-subtitle">Signed in as</div><div class="cp-person-name">{username}</div>', unsafe_allow_html=True)
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_id = None
        st.rerun()