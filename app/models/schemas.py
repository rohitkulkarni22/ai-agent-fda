from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QueryRequest(BaseModel):
    query: str

class MetaData(BaseModel):
    query_used: str
    total_reports: int
    sampled: int

class Citation(BaseModel):
    type: str
    url: str

class QueryResponseData(BaseModel):
    answer: str
    short_summary: str
    citations: List[Citation]
    meta: MetaData

class QueryResponse(BaseModel):
    status: str
    data: Optional[QueryResponseData] = None
    message: Optional[str] = None
