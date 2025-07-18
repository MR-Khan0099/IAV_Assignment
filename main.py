from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os
import base64
import uuid
from mdf_utils import load_mdf_signals
from llm_utils import generate_analysis_code_with_llm
from code_executor import execute_generated_code

UPLOAD_FOLDER = "mdf_uploads"
RESULTS_FOLDER = "results"

app = FastAPI()

# Ensure results folder exists
os.makedirs(RESULTS_FOLDER, exist_ok=True)

class AnalysisRequest(BaseModel):
    mdf_filename: str
    signal_descriptions: dict
    analysis_request: str

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    # 1. Build the MDF file path
    mdf_path = os.path.join(UPLOAD_FOLDER, request.mdf_filename)
    if not os.path.isfile(mdf_path):
        return JSONResponse({"error": f"MDF file '{request.mdf_filename}' not found in '{UPLOAD_FOLDER}'."}, status_code=404)

    # 2. Extract signal names from descriptions
    signal_names_to_extract = list(request.signal_descriptions.keys())

    # 3. Load data from MDF
    df = load_mdf_signals(mdf_path, signal_names_to_extract)

    if df is None:
        return JSONResponse({"error": "Failed to load data from MDF file."}, status_code=400)

    # 4. Generate Python code using LLM
    llm_generated_code = generate_analysis_code_with_llm(
        request.signal_descriptions,
        request.analysis_request,
        df.columns.tolist()
    )

    if not llm_generated_code:
        return JSONResponse({"error": "Could not generate analysis code."}, status_code=500)

    # Save the generated code to a file
    code_filename = f"analysis_{uuid.uuid4().hex}.py"
    code_path = os.path.join(RESULTS_FOLDER, code_filename)
    with open(code_path, "w", encoding="utf-8") as code_file:
        code_file.write(llm_generated_code)

    # 5. Execute the generated code safely
    analysis_result = execute_generated_code(llm_generated_code, df)

    # If the result is a base64 string (image), save and return as file, and include the code in the response
    if isinstance(analysis_result, str):
        image_filename = f"analysis_{uuid.uuid4().hex}.png"
        image_path = os.path.join(RESULTS_FOLDER, image_filename)
        with open(image_path, "wb") as f:
            f.write(base64.b64decode(analysis_result))
        # Commented out: direct file download only
        # return FileResponse(image_path, media_type="image/png", filename=image_filename)
        # Instead, return JSON with image path and code
        return {
            "image_file": image_path,
            "python_code_file": code_path,
            "python_code": llm_generated_code
        }
    else:
        # Otherwise, return as JSON (statistics)
        return {"analysis_result": analysis_result} 