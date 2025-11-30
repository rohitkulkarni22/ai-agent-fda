# FDA Food Adverse Event AI Agent

An AI agent that takes natural-language questions about foods/diets, queries the openFDA Food Adverse Event API, and uses OpenAI to synthesize a natural-language answer.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure environment:
   Copy `.env.example` to `.env` and add your OpenAI API key.
   ```bash
   cp .env.example .env
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

Send a POST request to `/v1/food-adverse-events/query`:

```json
{
  "query": "Are there FDA reports of people getting sick after eating corn chips?"
}
```

## Docker

Build and run with Docker:
```bash
docker build -t fda-agent .
docker run -p 8000:8000 --env-file .env fda-agent
```
