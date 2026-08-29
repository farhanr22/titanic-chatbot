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
        st.title("🚢 Titanic Analyst")
        st.markdown(
            "AI data analysis agent built using **FastAPI**, **LangChain**, and **Streamlit**. "
            "Equipped with **Pandas** and **Plotly** tools to query the dataset and generate visualizations."
        )

        with st.expander("📊 About the Dataset", expanded=False):
            st.markdown(
                """
                Contains information for **891** Titanic passengers, covering:
                - **Survival Outcome:** Alive / Dead
                - **Ticket Class:** 1st, 2nd, 3rd class
                - **Demographics:** Gender and Age
                - **Family Onboard:** Siblings, spouses, parents, children
                - **Ticket Fare:** Price paid for the journey
                - **Port of Embarkation:** Cherbourg, Queenstown, Southampton
                """
            )

        with st.expander("💡 Sample Prompts", expanded=False):
            st.markdown(
                """
                - *"How many passengers survived vs died?"*
                - *"What was the average fare paid across passenger classes?"*
                - *"Plot a bar chart of survival count by gender with custom colors."*
                - *"Show the age distribution across passenger classes as a violin plot."*
                - *"Calculate the survival rate for passengers traveling alone vs with family."*
                - *"Create an interactive sunburst chart showing Class → Gender → Survival breakdown."*
                """
            )

        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.caption("Developed by Farhan Rahaman.  \n**[View on GitHub](https://github.com/farhanr22/titanic-chatbot)**")
