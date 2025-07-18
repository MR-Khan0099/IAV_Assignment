# LLM-Driven MDF Analysis API

This project provides a REST API for analyzing measurement data from MDF files using signal descriptions and natural language analysis requests. The API uses an LLM to generate Python code for the requested analysis and executes it on the uploaded MDF data.

## Features
- Upload MDF files and request custom analyses (e.g., histograms, statistics) via natural language
- Uses asammdf, pandas, matplotlib, seaborn for data handling and plotting
- LLM (OpenAI/Gemini) generates analysis code
- Returns results as downloadable PNG images or JSON statistics
- **(Optional)** Can save and return the generated Python analysis code for transparency and reuse

## Setup

1. **Clone the repository** (or copy the files to a directory):

```
git clone <your-repo-url>
cd IAV
```

2. **Create and activate a virtual environment:**

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```
pip install -r requirements.txt
```

4. **Set your OpenAI API key:**

```
export OPENAI_API_KEY=sk-...your-key...
# Or use a .env file with OPENAI_API_KEY=sk-...your-key...
```

5. **Run the API server:**

```
uvicorn main:app --reload
```

## Usage

Send a POST request to `/analyze` with:
- `mdf_filename`: The MDF file to analyze (must be in `mdf_uploads/`)
- `signal_descriptions`: JSON object mapping signal names to descriptions
- `analysis_request`: Natural language string describing the analysis

### Example Request (using `curl`):

```
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "mdf_filename": "Vehicle01_meas4.mf4",
    "signal_descriptions": {
      "Eng_uBatt": "Battery voltage in mV",
      "Eng_nEng10ms": "Engine speed",
      "FuSHp_pRailBnk1": "Fuel Pressure"
    },
    "analysis_request": "a histogram of the battery voltage"
  }'
```

### API Response
- If the analysis produces a plot (e.g., histogram), the API returns a downloadable PNG image file.
- If the analysis produces statistics, the API returns a JSON object with the results.

#### **(Optional) Returning the Generated Python Code**
- The API can be configured to also save and return the generated Python analysis code.
- To enable this, uncomment the relevant code in `main.py` (see comments in the file).
- When enabled, the API response will include:
  - The path to the saved image file
  - The path to the saved Python code file
  - The generated Python code as a string

#### Example JSON Response (when code return is enabled):
```json
{
  "image_file": "results/analysis_abc123.png",
  "python_code_file": "results/analysis_abc123.py",
  "python_code": "def perform_analysis(df): ..."
}
```

## Testing
- Place your MDF files in the `mdf_uploads` folder in the project root.
- Use the `/docs` endpoint for interactive API documentation and testing.

## Obtaining MDF Test Data
- You can download sample MDF files from:
  - [ASAM MDF Example Files](https://www.asam.net/standards/detail/mdf/downloads/)
  - [GitHub: asammdf test files](https://github.com/danielhrisca/asammdf/tree/master/tests/testdata)
- Or use your own measurement data in MDF format.

## Notes
- The LLM code generation uses OpenAI by default. To use Gemini, see comments in `llm_utils.py`.
- For production, sandbox code execution for security.
- The API can be easily extended to support more analysis types or output formats.

## License
MIT

# MDF Upload Folder

Place your MDF files in the `mdf_uploads` folder in the project root. When making API requests, specify the filename (e.g., `example.mf4`) in the request body. The API will load the MDF file from this folder. 