from fastapi import APIRouter, HTTPException
import httpx
from config import GEMINI_API_KEY
from database import contracts_collection
from bson import ObjectId
from service.gemini_analysis import analyze_contract
from database import analysis_collection

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"]
)

@router.get("/contract/{contract_id}")
async def analysis_contract(contract_id:str):
    """
    Analyze a contract using AI and return insights
    """
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="AI API key is not configured")
    contract = contracts_collection.find_one({"_id":ObjectId(contract_id)})
    print(f"Contract: {contract}")
    if not contract:
        raise HTTPException(status_code=404,detail="Contract not found")
    if not contract.get("text_content"):
        raise HTTPException(status_code=400,detail="Contract has no text content to analyze")

    contracts_collection.update_one({"_id":ObjectId(contract_id)} , {"$set":{
        "analysis_status":"in_progress"
    }})

    try:
        result = await analyze_contract(contract_id, contract["text_content"])
    except httpx.TimeoutException as exc:
        contracts_collection.update_one(
            {"_id": ObjectId(contract_id)}, {"$set": {"analysis_status": "failed"}}
        )
        raise HTTPException(
            status_code=504,
            detail="The AI service took too long to analyze this contract. Please try again.",
        ) from exc

    doc = result.model_dump()
    insert_result = analysis_collection.insert_one(doc)

    result.id = str(insert_result.inserted_id)

    contracts_collection.update_one({"_id":ObjectId(contract_id)},{"$set":{"analysis_status":"completed"}})

    return {
        "message":"Contract analyzed successfully",
        "analysis": result.model_dump(),
        "id":result.id
    }

@router.get("/{analysis_id}")
def get_analysis(analysis_id:str):
    """
    Retrieve the results of a specific analysis by id
    """

    analysis = analysis_collection.find_one({"_id":ObjectId(analysis_id)})

    if not analysis:
        raise HTTPException(status_code=404,detail="Analysis not found")
    analysis["id"] = str(analysis.pop("_id"))
    return{
        "Analysis":analysis
    }

@router.get("/")
def list_analysis():
    """
    List all analyses performed
    """

    analyses = []
    for doc in analysis_collection.find({}):
        doc["id"] = str(doc.pop("_id"))
        analyses.append(doc)

    return {
        "analyses": analyses
    }
