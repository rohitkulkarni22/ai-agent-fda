import re

def extract_keywords(query: str) -> dict:
    """
    Extracts keywords from a natural language query using deterministic rules.
    Returns a dictionary with search clauses and limit.
    """
    query = query.lower()
    
    # Basic mapping for MVP
    # In a real app, this would be more comprehensive or use a better NLP approach
    mappings = {
        "corn chips": 'products.name_brand:"CORN+CHIPS"',
        "snack food": 'products.industry_name:"Snack+Food+Item"',
        "nausea": 'reactions:"NAUSEA"',
        "vomiting": 'reactions:"VOMITING"',
        "diarrhea": 'reactions:"DIARRHEA"',
        "headache": 'reactions:"HEADACHE"',
        "fever": 'reactions:"PYREXIA"', # Medical term for fever
        "rash": 'reactions:"RASH"',
    }
    
    search_clauses = []
    
    # Check for mapped terms
    for term, clause in mappings.items():
        if term in query:
            search_clauses.append(clause)
            
    # If no specific terms found, try to extract potential product names (very basic)
    # This is a fallback for the MVP to handle queries not in the mapping
    if not search_clauses:
        # Remove common stop words
        stop_words = ["are", "there", "fda", "reports", "of", "people", "getting", "sick", "after", "eating", "drinking", "about", "any", "issues", "with"]
        words = [w for w in re.findall(r'\w+', query) if w not in stop_words]
        if words:
             # Take the longest remaining word as a potential product/reaction guess if nothing else matches
             # This is weak but fits the "deterministic, no LLM" MVP constraint for now
             pass

    return {
        "search_clauses": search_clauses,
        "limit": 50
    }
