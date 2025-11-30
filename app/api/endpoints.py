from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import QueryRequest, QueryResponse, QueryResponseData, MetaData, Citation
from app.services.keyword_extractor import extract_keywords
from app.services.fda_client import FDAClient, construct_fda_query
from app.services.preprocessor import preprocess_fda_data
# from app.core.llm import generate_response # To be implemented

router = APIRouter()

@router.post("/food-adverse-events/query", response_model=QueryResponse)
async def query_food_events(request: QueryRequest):
    # 1. Extract keywords
    extraction_result = extract_keywords(request.query)
    search_clauses = extraction_result["search_clauses"]
    limit = extraction_result["limit"]
    
    # 2. Construct FDA query
    fda_query_string = construct_fda_query(search_clauses, limit)
    
    # 3. Query openFDA
    fda_client = FDAClient()
    try:
        fda_data = await fda_client.get_events(fda_query_string)
    finally:
        await fda_client.close()
        
    if fda_data is None:
        return QueryResponse(status="error", message="openFDA unavailable or error occurred.")

    # 4. Preprocess data
    summary = preprocess_fda_data(fda_data)
    
    # 5. Call LLM
    from app.core.llm import generate_response
    answer = await generate_response(request.query, fda_query_string, summary)
    
    # Extract short summary (naive approach for MVP, or ask LLM for it specifically)
    # For now, just take the first sentence or a default string
    short_summary = answer.split('.')[0] + "." if answer else "No summary available."
    
    return QueryResponse(
        status="ok",
        data=QueryResponseData(
            answer=answer,
            short_summary=short_summary,
            citations=[Citation(type="openfda", url=f"https://api.fda.gov/food/event.json?{fda_query_string}")],
            meta=MetaData(
                query_used=fda_query_string,
                total_reports=summary["total"],
                sampled=summary["sampled"]
            )
        )
    )
