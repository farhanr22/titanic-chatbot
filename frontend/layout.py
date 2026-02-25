import streamlit as st


def setup_page_layout():
    """Set up the page and all static UI components."""

    st.set_page_config(page_title="Titanic Chatbot", layout="centered", page_icon="🚢")

    render_custom_css()
    render_header()
    render_sidebar()


def render_custom_css():
    st.markdown(
        """
        <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:wght@400&family=News+Cycle:wght@400&display=swap');

        h1 * {
            font-family: 'Instrument Serif', serif !important;
            font-weight: 400 !important;
        }

        div.stChatMessage:has([aria-label="Chat message from user"]) {
            background-color: #dfeff0;
        }

        h1 span.sans{
            font-family: 'News Cycle', sans-serif !important;
            font-weight: 400 !important;
            font-size: 2.6rem;
        }

        p span.sans{
            font-family: 'News Cycle', sans-serif !important;
            font-size:1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        "<h1><span class='sans'>Chat with the</span> <em>RMS Titanic.</em></h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<span class='sans'>In 1912, the RMS Titanic sank in the midst of the North Atlantic Ocean.  \n"
        "It's 2026 now and this chatbot can answer your questions about it.</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<hr style='margin:0;margin-bottom:25px; border:0; border-top:1px solid darkblue;'>",
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.title("🛠️ Tech Stack")
        st.info("**Backend :** FastAPI on OCI")
        st.info("**Model :** GPT-OSS-120B")
        st.info("**Provider :** Krutrim Cloud")
        st.info("**Framework :** LangChain")
        st.write("---")
        st.caption("Developed by Farhan Rahaman for TailorTalk Internship Assignment.")
