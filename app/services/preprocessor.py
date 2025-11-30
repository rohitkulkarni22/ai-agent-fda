from typing import Dict, Any, List

def preprocess_fda_data(fda_json: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compacts the FDA JSON response to reduce token usage for the LLM.
    """
    if not fda_json or "results" not in fda_json:
        return {"total": 0, "sampled": 0, "reports": []}

    meta = fda_json.get("meta", {}).get("results", {})
    total = meta.get("total", 0)
    results = fda_json.get("results", [])
    
    compact_reports = []
    for item in results:
        report = {
            "report_number": item.get("report_number"),
            "date_created": item.get("date_created"),
            "reactions": item.get("reactions", []),
            "outcomes": item.get("outcomes", []),
            "products": []
        }
        
        for prod in item.get("products", []):
            report["products"].append({
                "name_brand": prod.get("name_brand"),
                "industry_name": prod.get("industry_name"),
                "role": prod.get("role")
            })
            
        compact_reports.append(report)

    return {
        "total": total,
        "sampled": len(compact_reports),
        "reports": compact_reports
    }
