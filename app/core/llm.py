from openai import AsyncOpenAI
from app.core.config import settings
import json

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You summarize openFDA Food Adverse Event data.
Provide factual, cautious, FDA-backed insights.
Never give medical advice. Avoid claims of causality.
Explain data limitations clearly.

Input will be a JSON object containing:
- user_query: The original question from the user.
- fda_query: The query string used to fetch data from openFDA.
- fda_summary: A summarized version of the FDA data.

Output should be a natural language response.
"""

async def generate_response(user_query: str, fda_query: str, fda_summary: dict) -> str:
    """
    Calls OpenAI to generate a synthesized response based on FDA data.
    """
    if not settings.OPENAI_API_KEY:
        return "OpenAI API key not configured. Cannot generate response."

    user_content = json.dumps({
        "user_query": user_query,
        "fda_query": fda_query,
        "fda_summary": fda_summary
    }, indent=2)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo depending on availability/cost
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3, # Low temperature for factual responses
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response from LLM: {str(e)}"
