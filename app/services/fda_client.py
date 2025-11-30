import httpx
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

FDA_API_URL = "https://api.fda.gov/food/event.json"

class FDAClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_events(self, query_string: str) -> Optional[Dict[str, Any]]:
        """
        Queries the openFDA Food Adverse Event API.
        """
        url = f"{FDA_API_URL}?{query_string}"
        logger.info(f"Querying FDA API: {url}")
        
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.info("No records found for query.")
                return {"meta": {"results": {"total": 0}}, "results": []}
            logger.error(f"FDA API HTTP error: {e}")
            return None
        except Exception as e:
            logger.error(f"FDA API error: {e}")
            return None

    async def close(self):
        await self.client.aclose()

def construct_fda_query(search_clauses: list, limit: int = 50) -> str:
    """
    Constructs the openFDA query string from search clauses.
    """
    if not search_clauses:
        return ""
        
    search_param = "+AND+".join(search_clauses)
    return f"search={search_param}&limit={limit}"
