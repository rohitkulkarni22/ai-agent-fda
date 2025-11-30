
# FDA Food Adverse Event AI Agent – MVP PRD (Updated for Python 3 + FastAPI + OpenAI SDK)

## 0. Document Info

- **Product name:** FDA Food Adverse Event AI Agent
- **Version:** v0.2 (MVP Updated)
- **Owner:** AI / Data Engineering
- **Primary LLM:** OpenAI API (GPT‑5.1, GPT‑4o, etc.)
- **Backend Stack:** Python 3 + FastAPI
- **External data source:** openFDA Food Adverse Event API (`/food/event`)
- **LLM Usage:** **Single OpenAI model call per user query** (for final synthesis)

---

## 1. Overview

### 1.1 Goal

Build an AI agent that takes any **natural‑language question about foods, diets, or FDA adverse events**, and:

1. Receives a user query in plain language.
2. Extracts keywords using rule‑based NLP (deterministic, no LLM).
3. Constructs an **openFDA-compliant query**.
4. Calls the **openFDA Food Event API**.
5. Preprocesses & compacts the FDA JSON.
6. Calls **OpenAI LLM once**:
   - Inputs: user query + FDA data + constructed FDA query.
   - Output: synthesized FDA‑backed explanation.
7. Returns a natural-language answer including:
   - FDA data summary
   - insights
   - citations
   - safety disclaimers

---

## 2. Tech Stack (Updated)

### **Backend**
- **Python 3+**
- **FastAPI** (async API server)
- **Uvicorn** (ASGI server)

### **LLM Client**
- **OpenAI Python SDK**
  - Supports: GPT‑5.1, GPT‑4o-mini, o-series, JSON mode, etc.

### **FDA Data Source**
- **openFDA Food Adverse Event API**
  - `https://api.fda.gov/food/event.json`

### **Other Tools**
- `httpx` (async HTTP client)
- `pydantic` (data validation)
- `python-dotenv` (env config)
- `pytest` (optional, for API tests)
- Postman / curl for manual testing

---

## 3. Functional Workflow (Single LLM Call)

### **High‑Level Steps**

1. **User → FastAPI**  
   Input: natural-language query.
2. **Rule-based keyword extraction**  
   - Identify product names  
   - Food categories  
   - Reaction terms  
3. **Construct FDA query string**
4. **FastAPI → openFDA API**
5. **Preprocess returned JSON**
6. **FastAPI → OpenAI LLM**  
   - Provide:
     - original query  
     - constructed FDA query  
     - FDA summarized JSON  
7. **LLM → synthesized output**
8. **FastAPI → User**
   - Structured JSON
   - citations
   - limitations disclaimer

---

## 4. FastAPI Endpoint Design

### POST `/v1/food-adverse-events/query`

#### Request Body
```json
{
  "query": "Are there FDA reports of people getting sick after eating corn chips?"
}
```

#### Response Body (success)
```json
{
  "status": "ok",
  "data": {
    "answer": "...natural language FDA-backed summary...",
    "short_summary": "...",
    "citations": [ { "type": "openfda", "url": "..." } ],
    "meta": {
      "query_used": "search=products.name_brand:"CORN+CHIPS"...",
      "total_reports": 1605,
      "sampled": 50
    }
  }
}
```

---

## 5. Keyword Extraction (Deterministic, No LLM)

### Techniques:
- Lowercasing
- Tokenizing
- Removing punctuation
- Mapping:
  - "corn chips" → `products.name_brand`
  - "snack food" → `products.industry_name`
  - reactions (“nausea”, “vomiting”, etc)

### Output Example:
```json
{
  "search_clauses": [
    "products.name_brand:"CORN+CHIPS"",
    "reactions:"NAUSEA""
  ],
  "limit": 50
}
```

---

## 6. FDA Query Construction

Example:
```
https://api.fda.gov/food/event.json
?search=products.name_brand:"CORN+CHIPS"+AND+reactions:"NAUSEA"
&limit=50
```

### Query Rules:
- Use `+AND+` between clauses.
- URL‑encode spaces as `+`.
- Default limit: 50 (adjustable).

---

## 7. openFDA API Integration

### Use **httpx.AsyncClient**:

- async GET request
- retry logic (2 retries)
- handle:
  - 200 responses
  - 4xx bad queries
  - 5xx FDA downtime
- MVP: only first page (no pagination)

### Fields of interest:
- `report_number`
- `date_created`
- `products` (brand, industry, role)
- `reactions`
- `outcomes`
- `consumer.gender`

---

## 8. Data Preprocessing Before LLM Call

### Goals:
- reduce token usage
- keep only relevant information
- turn raw FDA JSON → compact summary

### Preprocessed Structure Example:
```json
{
  "total": 1605,
  "sampled": 50,
  "reports": [
    {
      "report_number": "157840",
      "reactions": ["NAUSEA", "ABDOMINAL PAIN"],
      "products": [
        { "name_brand": "CORN CHIPS", "industry_name": "Snack Food Item" }
      ],
      "outcomes": ["Other Outcome"]
    }
  ]
}
```

---

## 9. Single OpenAI LLM Call (Synthesis Only)

### Input to OpenAI Model:
1. Original user query  
2. Constructed FDA query  
3. Preprocessed FDA JSON  
4. System prompt describing constraints  
5. Safety guidelines

### Output:
- FDA‑based synthesis
- limitations
- no medical advice
- citations
- short summary

### Example Prompt Skeleton

**system:**
```
You summarize openFDA Food Adverse Event data.
Provide factual, cautious, FDA-backed insights.
Never give medical advice. Avoid claims of causality.
Explain data limitations clearly.
```

**user:**
```json
{
  "user_query": "...",
  "fda_query": "...",
  "fda_summary": { ... }
}
```

---

## 10. Safety Rules

- Never provide medical advice, diagnosis, or treatment.
- Always add a safety disclaimer:
  > FDA adverse event reports do not prove causality and may be under-reported.
- If user asks medical questions:  
  → return safety message without LLM call

---

## 11. API Response Format

```json
{
  "status": "ok",
  "data": {
    "answer": "...",
    "short_summary": "...",
    "citations": [],
    "meta": {}
  }
}
```

Error example:

```json
{
  "status": "error",
  "message": "openFDA unavailable. Try again later."
}
```

---

## 12. System Architecture (Updated)

### Components:

- **FastAPI backend**
- **openFDA client (httpx)**
- **OpenAI LLM client**
- **Keyword extraction module**
- **Preprocessing module**
- **Logging & metrics**

### Sequence:

1. User → FastAPI
2. FastAPI → keyword parser
3. FastAPI → openFDA
4. FastAPI → preprocess
5. FastAPI → OpenAI (one call)
6. FastAPI → User

---

## 13. Deployment

- Docker container (Python 3 + FastAPI)
- ASGI server: Uvicorn
- Easily deployable to:
  - AWS ECS / EC2
  - GCP Cloud Run
  - Azure App Service
  - Railway / Render
  - Vercel (Python functions)

---

## 14. MVP Delivery Checklist

- [ ] FastAPI endpoint created  
- [ ] Deterministic keyword extractor  
- [ ] FDA query builder  
- [ ] openFDA integration  
- [ ] Preprocessing step  
- [ ] Single OpenAI call wired up  
- [ ] Logging & metrics  
- [ ] Dockerfile  
- [ ] Basic Postman collection  
- [ ] README  

---

## 15. Success Criteria

- ≥80% accuracy in summarizing FDA data (spot‑checked)
- All answers include citations
- No medical advice in any response
- P95 latency < 5 seconds
- API stable during 100 consecutive calls

---

_End of PRD v0.2 (Python + FastAPI + OpenAI SDK update)_
