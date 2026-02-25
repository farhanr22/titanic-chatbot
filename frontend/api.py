import requests
import streamlit as st


def query_agent_api(user_input: str, session_id: str) -> dict:
    """Sends the user query to the backend agent and returns the parsed response."""

    api_url = st.secrets["API_URL"]
    headers = {"Authorization": f"Bearer {st.secrets['API_TOKEN']}"}
    payload = {"user_input": user_input, "session_id": session_id}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=60)

        try:
            return response.json()

        except ValueError:
            return {
                "success": False,
                "error": {
                    "message": f"Server Error ({response.status_code})",
                    "details": response.text
                    or "The server returned an invalid non-JSON response.",
                },
            }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": {
                "message": "Backend server is unreachable.",
                "details": "Connection refused. Please ensure the backend API is running.",
            },
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": {
                "message": "Request Timed Out.",
                "details": "The AI agent took longer than 60 seconds to respond. Please try again.",
            },
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": {"message": "A network error occurred.", "details": str(e)},
        }
