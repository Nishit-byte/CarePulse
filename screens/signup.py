import streamlit as st
from database import add_user

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    #MainMenu, header, footer { visibility: hidden; }
    .stApp { background: #9FC9CF; }
    .block-container {
        display: block !important;
        margin: 0 auto !important;
        max-width: 460px !important;
        width: 100% !important;
        padding-top: 3rem !important;
    }
    .cp-signup-title {
        font-weight: 300;
        font-size: clamp(1.6rem, 6vw, 2.2rem);
        letter-spacing: 0.25em;
        color: #111111;
        text-align: center;
        white-space: nowrap;
        margin-bottom: 1.6rem;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #37507B !important;
        border-radius: 24px !important;
        border: none !important;
        padding: 2rem 1.8rem !important;
    }
    .stTextInput input {
        background-color: #14B8C4 !important;
        color: #111111 !important;
        border: none !important;
        border-radius: 999px !important;
        text-align: center !important;
        font-weight: 500 !important;
        padding: 0.7rem 1rem !important;
    }
    .stTextInput label { display: none; }
    .stFormSubmitButton button {
        background-color: #14B8C4 !important;
        color: #111111 !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 0.7rem 0 !important;
    }
    .cp-link-row { text-align: center; margin-top: 1.4rem; }
    .cp-link-row button {
        background: transparent !important;
        color: #1A2135 !important;
        border: none !important;
        font-weight: 600 !important;
        text-decoration: underline !important;
    }
    </style>
    <div class="cp-signup-title">Create Account</div>
    """,
    unsafe_allow_html=True
)

with st.container(border=True):
    with st.form("signup_form", border=False):
        username = st.text_input("Username", placeholder="Username")
        email = st.text_input("Email", placeholder="Email")
        password = st.text_input("Password", placeholder="Password", type="password")
        confirm = st.text_input("Confirm Password", placeholder="Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if not username or not password:
                st.error("Username and password are required.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                user_id = add_user(username, email, password)
                if user_id:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_id = user_id
                    st.rerun()
                else:
                    st.error("That username is already taken.")

st.markdown('<div class="cp-link-row">', unsafe_allow_html=True)
if st.button("← Already have an account? Log in", key="signup_to_login"):
    st.switch_page("screens/login.py")
st.markdown('</div>', unsafe_allow_html=True)