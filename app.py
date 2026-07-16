import streamlit as st
from database import init_db

st.set_page_config(page_title="CarePulse", page_icon="💛", layout="wide")
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

landing_page = st.Page("screens/landing.py", title="Welcome", url_path="landing")
login_page = st.Page("screens/login.py", title="Log In", url_path="login")
signup_page = st.Page("screens/signup.py", title="Sign Up", url_path="signup")

dashboard_page = st.Page("screens/dashboard.py", title="Dashboard", icon="🏠", url_path="dashboard", default=True)
alerts_page = st.Page("screens/alerts.py", title="Alerts", icon="🔔", url_path="alerts")
history_page = st.Page("screens/history.py", title="History", icon="🕐", url_path="history")
users_page = st.Page("screens/users.py", title="Users", icon="👥", url_path="users")
devices_page = st.Page("screens/devices.py", title="Devices", icon="📷", url_path="devices")
reports_page = st.Page("screens/reports.py", title="Reports", icon="📊", url_path="reports")
settings_page = st.Page("screens/settings.py", title="Settings", icon="⚙️", url_path="settings")

if st.session_state.logged_in:
    nav = st.navigation(
        {
            "CarePulse": [dashboard_page, alerts_page, history_page, users_page, devices_page, reports_page, settings_page],
        }
    )
else:
    nav = st.navigation([landing_page, login_page, signup_page])

nav.run()