import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from langchain_core.tools import tool
from app.core.logging import app_logger


GLOBAL_DF = None


def load_global_df():
    """Load the DataFrame into memory once"""
    global GLOBAL_DF
    if GLOBAL_DF is None:
        GLOBAL_DF = pd.read_csv("/data/titanic.csv")


def get_repl_locals():
    load_global_df()
    return {"px": px, "go": go, "df": GLOBAL_DF}


@tool(response_format="content_and_artifact")
def python_plot_tool(code: str) -> tuple[str, str]:
    """
    Executes Python code to generate a Plotly figure.
    You already have access to 'px' (plotly.express), 'go' (plotly.graph_objects), and 'df' (Titanic DataFrame). DO NOT IMPORT THESE.
    You MUST assign the final Plotly figure object to a variable named EXACTLY 'fig'.
    Do NOT call fig.show().
    """
    repl_locals = get_repl_locals()
    try:
        # NOTE : Can be dangerous.
        exec(code, {}, repl_locals)
        app_logger.info(f"Plot Tool Code executed: {code}")

        if "fig" in repl_locals:
            fig = repl_locals["fig"]
            fig_json = fig.to_json(engine="json")
            return "Success: Plot generated and captured.", fig_json
        else:
            return (
                "Error: You ran the code, but forgot to assign the plot to the 'fig' variable. Fix it.",
                "",
            )
    except Exception as e:
        app_logger.error(f"Plot Tool Error: {e}")
        return f"Error executing code: {str(e)}", ""


@tool
def python_data_tool(code: str) -> str:
    """
    Executes Python code to analyze the Titanic dataset.
    You have access to the pandas DataFrame as 'df'.
    You MUST assign the final answer or computed value to a variable named EXACTLY 'result'.
    """
    repl_locals = get_repl_locals()
    try:
        # NOTE : Can be dangerous.  
        exec(code, {}, repl_locals)
        app_logger.info(f"Data Tool Code executed: {code}")

        if "result" in repl_locals:
            result_val = str(repl_locals["result"])
            return f"Computation successful. Result: \n{result_val}"
        else:
            return "Error: You forgot to assign the final output to the 'result' variable. Fix it."
    except Exception as e:
        app_logger.error(f"Data Tool Error: {e}")
        return f"Error executing code: {str(e)}"


tools = [python_plot_tool, python_data_tool]
