import os
import openai
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key as an environment variable: OPENAI_API_KEY
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def extract_code_block(text):
    """Extracts the first Python code block from LLM response."""
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_analysis_code_with_llm(signal_descriptions: dict, analysis_request: str, available_columns: list):
    """
    Uses OpenAI LLM to generate Python code for data analysis.
    Returns the code as a string (function perform_analysis(df)).
    """
    prompt = f"""
You are an expert Python data analyst. Your task is to generate Python code to analyze measurement data.
The data is provided as a pandas DataFrame named 'df'.
The available columns in the DataFrame are: {available_columns}.
Here are the descriptions of the signals:
{signal_descriptions}

The user wants to perform the following analysis: \"{analysis_request}\".

Generate Python code that performs this analysis.
If the analysis requires a plot (e.g., histogram, line plot), generate code that saves the plot to a BytesIO object as a PNG image and then encodes it in base64.
If the analysis requires statistical summary (e.g., min/max/avg), return a dictionary with the results.
The code should be a single function named `perform_analysis(df)` that returns either a base64 string (for images) or a dictionary (for statistics).
Do NOT include any `import` statements within the function, assume `pandas`, `matplotlib.pyplot`, `seaborn`, `io`, and `base64` are already imported.
Do NOT include any example usage or explanations, only the function definition.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for better results
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        generated_code = response.choices[0].message.content
        return extract_code_block(generated_code)
    except Exception as e:
        print(f"Error generating code with LLM: {e}")
        return None

# ---
# To use Google Gemini instead, comment out the OpenAI section above and use:
# import google.generativeai as genai
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# def generate_analysis_code_with_llm(...):
#     ... 

