import streamlit as st
import base64
import os

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

encoded_image = get_base64_image("data/family_hero.png")

if encoded_image:
    image_css = f"background-image: url('data:image/jpeg;base64,{encoded_image}'); background-size: cover; background-position: center;"
else:
    image_css = "background: linear-gradient(135deg, #B8C4C8 0%, #8FA3A8 100%);"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&family=Caveat:wght@500;600&display=swap');

    html, body, [class*="css"] {{ font-family: 'Poppins', sans-serif; }}
    #MainMenu, header, footer {{ visibility: hidden; }}
    .stApp {{ background: #E6E6E6; }}

    .block-container {{
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        margin-left: 46vw !important;
        margin-right: 0 !important;
        width: 54vw !important;
        max-width: 54vw !important;
        min-height: 100vh !important;
        padding: 2rem 3rem !important;
        box-sizing: border-box !important;
    }}

    .cp-side-image {{
        position: fixed;
        top: 0;
        left: 0;
        width: 46vw;
        height: 100vh;
        {image_css}
        z-index: 0;
    }}

    .cp-side-placeholder-text {{
        position: fixed;
        top: 50%;
        left: 23vw;
        transform: translate(-50%, -50%);
        color: #4A5A5D;
        font-weight: 500;
        font-size: 0.9rem;
        text-align: center;
        z-index: 1;
        display: {"none" if encoded_image else "block"};
    }}

    .cp-wordmark {{
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
        font-size: clamp(1.6rem, 3.6vw, 2.8rem);
        letter-spacing: 0.22em;
        color: #111111;
        text-align: center;
        white-space: nowrap;
        margin-bottom: 0.6rem;
    }}

    .cp-tagline {{
        font-family: 'Caveat', cursive;
        font-weight: 600;
        font-size: 1.5rem;
        color: #222222;
        text-align: center;
        margin-bottom: 2.4rem;
    }}

    .stButton button {{
        background-color: #14B8C4 !important;
        color: #111111 !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 0.65rem 0 !important;
        width: 100% !important;
    }}
    .stButton button:hover {{ background-color: #11A3AE !important; }}

    .cp-contact {{
        position: fixed;
        bottom: 2.5rem;
        left: calc(46vw + 3rem);
        text-align: left;
        z-index: 2;
    }}
    .cp-contact-title {{ font-size: 1.3rem; color: #111111; font-weight: 500; margin-bottom: 0.3rem; }}
    .cp-contact-line {{ font-size: 0.95rem; color: #333333; font-weight: 400; }}
    </style>

    <div class="cp-side-image"></div>
    <div class="cp-side-placeholder-text">Add your own photo at<br><code>assets/family_photo.jpg</code></div>

    <div class="cp-wordmark">C a r e P u l s e</div>
    <div class="cp-tagline">Watching the vectors that keep them safe</div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Login", key="landing_login"):
        st.switch_page("screens/login.py")
    if st.button("Sign up", key="landing_signup"):
        st.switch_page("screens/signup.py")

st.markdown(
    """
    <div class="cp-contact">
        <div class="cp-contact-title">Contact Us</div>
        <div class="cp-contact-line">Phone</div>
        <div class="cp-contact-line">Email</div>
    </div>
    """,
    unsafe_allow_html=True
)