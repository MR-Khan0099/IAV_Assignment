import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd

def execute_generated_code(code_string: str, df: pd.DataFrame):
    """
    Executes the generated Python code safely.
    WARNING: Executing arbitrary code can be a security risk.
    This implementation is for demonstration and should be
    replaced with a more robust sandboxing solution in production.
    """
    try:
        exec_globals = {
            'df': df,
            'pd': pd,
            'plt': plt,
            'sns': sns,
            'io': io,
            'base64': base64,
        }
        exec_locals = {}
        exec(code_string, exec_globals, exec_locals)
        if 'perform_analysis' in exec_locals:
            result = exec_locals['perform_analysis'](df)
            return result
        else:
            return {"error": "Generated code did not define 'perform_analysis' function."}
    except Exception as e:
        print(f"Error executing generated code: {e}")
        return {"error": f"Error during analysis: {e}"} 