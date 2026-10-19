# Legal Contract Analyzer

Upload a PDF or plain text contract, extract its text, and use Google Gemini to produce a structured analysis of its clauses and potential risks. The API is built with **FastAPI** and stores contracts and analysis results in **MongoDB**.

> **Note:** This project provides AI-generated information for review. It is not legal advice and should not replace advice from a qualified lawyer.

## What it does

- Accepts PDF and TXT uploads up to 10 MB.
- Extracts contract text and records basic document details.
- Analyzes contract text with Gemini, including summaries, key clauses, risk flags, and recommendations.
- Stores contracts and analysis results in MongoDB.
- Provides endpoints to retrieve contracts and analysis results.
- Exposes interactive API documentation through Swagger UI.

## Requirements

- Python (the project has been run with Python 3.14)
- Docker Desktop or a local MongoDB instance
- A Google AI API key with access to the Gemini API

## Setup

### 1. Start MongoDB

From the project root, start the MongoDB service defined in `docker-compose.yml`:

```bash
docker compose up -d
```

The compose file exposes MongoDB on `localhost:27017` and creates a root user with the credentials configured in that file.

### 2. Create and activate a virtual environment

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Configure environment variables

Create `app/.env` with your local settings:

```dotenv
MONGODB_URI=mongodb://root:mypassword@localhost:27017/mydb?authSource=admin
GOOGLE_AI_API_KEY=your_google_ai_api_key
```

Replace the sample MongoDB credentials if you changed `docker-compose.yml`. Keep `app/.env` private; do not commit secrets.

### 4. Run the API

The application uses imports relative to the `app` directory. Start Uvicorn from there:

```bash
cd app
../.venv/bin/uvicorn main:app --reload
```

The API will be available at <http://127.0.0.1:8000>.

## API reference

Interactive documentation is available at:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Show the service welcome message and version. |
| `POST` | `/contracts/upload` | Upload and extract a PDF or TXT contract. |
| `GET` | `/contracts/` | List contracts without their extracted text. |
| `GET` | `/contracts/{contract_id}` | Retrieve one contract, including extracted text. |
| `GET` | `/analysis/contract/{contract_id}` | Analyze a contract with Gemini and save the result. |
| `GET` | `/analysis/` | List saved analysis results. |
| `GET` | `/analysis/{analysis_id}` | Retrieve one saved analysis result. |

### Upload a contract

Use `multipart/form-data` with a field named `file`:

```bash
curl -X POST http://127.0.0.1:8000/contracts/upload \
  -F "file=@/path/to/contract.pdf"
```

The response includes the uploaded contract and its MongoDB ID. Use that ID to retrieve the contract or request an analysis.

### Analyze a contract

```bash
curl http://127.0.0.1:8000/analysis/contract/<contract_id>
```

The response contains a summary, contract type, key clauses, risk flags, overall risk level, and recommendations. Analysis sends up to the first 15,000 characters of extracted text to Gemini.

### Retrieve saved analyses

```bash
curl http://127.0.0.1:8000/analysis/<analysis_id>
curl http://127.0.0.1:8000/analysis/
```

## Project layout

```text
.
├── app/
│   ├── main.py                  # FastAPI application and router registration
│   ├── config.py                # Environment-based configuration
│   ├── database.py              # MongoDB client and collections
│   ├── models.py                # Pydantic data models
│   ├── routes/
│   │   ├── contracts.py         # Contract upload and retrieval endpoints
│   │   └── analysis.py          # Contract analysis and result endpoints
│   ├── service/
│   │   ├── document_parser.py   # PDF and TXT text extraction
│   │   ├── gemini_analysis.py   # Gemini request and result parsing
│   │   └── prompt.py            # Contract analysis prompt
│   └── uploads/                 # Uploaded files (created when needed)
├── docker-compose.yml           # Local MongoDB service
└── requirements.txt             # Python dependencies
```

## Current limitations

- PDF extraction depends on selectable text; scanned image PDFs may need OCR before they can be analyzed.
- The analysis request is synchronous from the API client's perspective and may take time while Gemini responds.
- Only PDF and TXT files are accepted, with a 10 MB upload limit.
- The analyzer truncates extracted contract text to 15,000 characters before sending it to Gemini.

## License

No license is currently specified. Add a `LICENSE` file before distributing or reusing this project.
