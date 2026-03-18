import streamlit as st
import uuid
import json
import plotly.graph_objs as go


from layout import setup_page_layout
from api import query_agent_api

# Set up the static components and layout
setup_page_layout()

# Check user authorization
query_user = st.query_params.get("user")
valid_user = st.secrets.get("USERNAME")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Display chat history
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(
        msg["role"], avatar="✨" if msg["role"] == "assistant" else "👤"
    ):
        st.write(msg["content"])
        if msg.get("figure"):
            st.plotly_chart(
                msg["figure"], use_container_width=True, key=f"history_plot_{i}"
            )


# Chat input with authorization logic
# If USERNAME secret is not set, skip validation and allow public access
auth_enabled = valid_user is not None

if auth_enabled:
    if not query_user:
        st.warning("⚠️ You need a valid user parameter to use this chatbot.")
    elif query_user != valid_user:
        st.error("❌ Invalid user.")

if auth_enabled and not query_user:
    user_input = st.chat_input(
        "You need a valid user parameter to use this chatbot.", disabled=True
    )
elif auth_enabled and query_user != valid_user:
    user_input = st.chat_input("Invalid user", disabled=True)
else:
    user_input = st.chat_input("Ask about the Titanic dataset...", disabled=False)

# Process chat input
if user_input:
    # Display user input immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)

    # Process and display assistant response
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Working on it..."):
            # API Call
            response_data = query_agent_api(user_input, st.session_state.session_id)

            if response_data.get("success"):
                data = response_data.get("data", {})
                final_text = data.get("text", "(No text output provided)")
                artifact_data = data.get("artifact")  # Check for plot data

                st.markdown(final_text)

                # Try to render the plot
                restored_fig = None
                if artifact_data:
                    try:
                        # Try to deserialize the JSON payload into a figure object
                        restored_fig = go.Figure(json.loads(artifact_data))
                        st.plotly_chart(
                            restored_fig,
                            use_container_width=True,
                            key=f"new_plot_{len(st.session_state.messages)}",
                        )
                    except Exception as e:
                        st.error(f"Failed to render plot.\n\n**Error:**  \n`{e}`")

                # Update chat history
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_text,
                        "figure": restored_fig,
                    }
                )
            else:
                error_msg = response_data.get("error", {}).get(
                    "message", "Unknown error"
                )
                error_details = response_data.get("error", {}).get("details", "")
                st.error(
                    f"Agent Error: {error_msg}.\n\n**Details:**  \n`{error_details}`"
                )
