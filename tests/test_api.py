from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, AsyncMock

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FDA Food Adverse Event AI Agent API"}

@patch("app.api.endpoints.FDAClient")
@patch("app.core.llm.generate_response")
def test_query_food_events(mock_generate_response, mock_fda_client):
    # Mock FDA Client
    mock_instance = mock_fda_client.return_value
    mock_instance.get_events = AsyncMock(return_value={
        "meta": {"results": {"total": 100}},
        "results": [
            {
                "report_number": "123",
                "reactions": ["NAUSEA"],
                "products": [{"name_brand": "TEST CHIPS", "industry_name": "Snack", "role": "Suspect"}]
            }
        ]
    })
    mock_instance.close = AsyncMock()

    # Mock LLM response
    mock_generate_response.return_value = "This is a test response. It mentions FDA data."

    response = client.post("/v1/food-adverse-events/query", json={"query": "test chips"})
    
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["answer"] == "This is a test response. It mentions FDA data."
    assert data["meta"]["total_reports"] == 100
    assert len(data["citations"]) > 0
    assert "api.fda.gov" in data["citations"][0]["url"]

@patch("app.api.endpoints.FDAClient")
def test_query_food_events_no_results(mock_fda_client):
    # Mock FDA Client returning None (error or no data)
    mock_instance = mock_fda_client.return_value
    mock_instance.get_events = AsyncMock(return_value=None)
    mock_instance.close = AsyncMock()

    response = client.post("/v1/food-adverse-events/query", json={"query": "unknown food"})
    
    assert response.status_code == 200
    assert response.json()["status"] == "error"
