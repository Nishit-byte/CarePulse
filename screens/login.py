import streamlit as st
from database import verify_user

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    #MainMenu, header, footer { visibility: hidden; }
    .stApp { background: #9FC9CF; }

    .block-container {
        display: block !important;
        flex-direction: unset !important;
        align-items: unset !important;
        justify-content: unset !important;
        margin: 0 auto !important;
        max-width: 460px !important;
        width: 100% !important;
        min-height: auto !important;
        padding-top: 4rem !important;
    }

    .cp-login-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
        font-size: clamp(1.8rem, 6vw, 2.6rem);
        letter-spacing: 0.3em;
        color: #111111;
        text-align: center;
        white-space: nowrap;
        margin-bottom: 2.2rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #37507B !important;
        border-radius: 24px !important;
        border: none !important;
        padding: 2rem 1.8rem !important;
        width: 100% !important;
    }

    .stTextInput input {
        background-color: #14B8C4 !important;
        color: #111111 !important;
        border: none !important;
        border-radius: 999px !important;
        text-align: center !important;
        font-weight: 500 !important;
        padding: 0.7rem 1rem !important;
        width: 100% !important;
    }
    .stTextInput input::placeholder { color: #0A3A3E !important; opacity: 0.75; }
    .stTextInput label { display: none; }
    .stTextInput > div { width: 100% !important; }

    .stFormSubmitButton button {
        background-color: #14B8C4 !important;
        color: #111111 !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 0.7rem 0 !important;
    }
    .stFormSubmitButton button:hover { background-color: #11A3AE !important; }

    .cp-link-row {
        text-align: center;
        margin-top: 1.4rem;
    }
    .cp-link-row button {
        background: transparent !important;
        color: #1A2135 !important;
        border: none !important;
        font-weight: 600 !important;
        text-decoration: underline !important;
        width: auto !important;
        padding: 0.3rem 0.6rem !important;
    }
    </style>

    <div class="cp-login-title">L o g i n</div>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):
    with st.form("login_form", border=False):
        username = st.text_input("Username", placeholder="Username")
        password = st.text_input("Password", placeholder="Password", type="password")
        submitted = st.form_submit_button("Submit")

        if submitted:
            user = verify_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.user_id = user["id"]
                st.rerun()
            else:
                st.error("Incorrect username or password.")

st.markdown('<div class="cp-link-row">', unsafe_allow_html=True)
if st.button("← Back to home", key="login_back"):
    st.switch_page("screens/landing.py")
if st.button("Don't have an account? Sign up", key="login_to_signup"):
    st.switch_page("screens/signup.py")
st.markdown('</div>', unsafe_allow_html=True)