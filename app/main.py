from fastapi import FastAPI
from database import init_db
from routes.contracts import router as contract_router
from routes.analysis import router as analysis_router

app = FastAPI(
    title="Legal Contract Analyzer",
    description="AI-Powered Contract Analysis using Gemini",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(contract_router)
app.include_router(analysis_router)

@app.get("/")
def root():
    return {
        "message":"Welcome to Legal Contract Analyzer",
        "version":"1.0.0"
    }