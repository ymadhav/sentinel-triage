import json
import requests
import os
import sys

# Ensure the module can find its own siblings in the 'src' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.knowledge_base import retrieve_context

def triage_ticket(ticket_issue, ticket_subject, company):
    """
    Analyzes a support ticket using local Llama 3.2 and grounded context.
    Ensures output matches the required Hackathon schema perfectly.
    """
    
    # 1. Retrieve grounded context from the local support corpus
    # If company is 'None', the knowledge base will search across all domains
    context = retrieve_context(ticket_issue, company)
    
    # 2. Schema-Strict Prompt for HackerRank Orchestrate
    prompt = f"""
    Analyze this support ticket based ONLY on the provided support corpus context.
    
    Target Company: {company}
    Subject: {ticket_subject}
    Issue: {ticket_issue}
    Corpus Context: {context}

    INSTRUCTIONS:
    1. If Company is 'None' or 'General', infer the correct company (HackerRank, Claude, or Visa) from the issue text.
    2. If the issue is entirely unrelated to these three companies, set status to 'escalated' and response to 'Out of Scope'.
    3. Determine if the case involves sensitive data or high-risk billing/access issues.
    
    REQUIRED JSON OUTPUT (Strict Schema):
    {{
      "status": "replied" or "escalated",
      "product_area": "string (e.g., Billing, API, Account Access)",
      "response": "User-facing answer grounded in the corpus",
      "justification": "Concise reasoning for the classification",
      "request_type": "product_issue", "feature_request", "bug", or "invalid"
    }}
    """

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        # Request inference from local Ollama server
        response = requests.post(url, json=payload, timeout=45)
        response.raise_for_status()
        result = response.json()
        
        # Parse the JSON response from the model
        raw_output = json.loads(result['response'])
        
        # 3. NORMALIZATION LAYER: Force Hackathon compliance
        # This prevents the agent from failing automated grading due to casing or invalid types.
        
        # Validate Status (must be 'replied' or 'escalated')
        final_status = str(raw_output.get("status", "escalated")).lower().strip()
        if final_status not in ["replied", "escalated"]:
            final_status = "escalated"
            
        # Validate Request Type (allowed: product_issue, feature_request, bug, invalid)
        allowed_types = ["product_issue", "feature_request", "bug", "invalid"]
        raw_type = str(raw_output.get("request_type", "product_issue")).lower().replace(" ", "_")
        
        # Map any hallucinations or internal flags to the official list
        if raw_type == "security_threat":
            final_type = "invalid"
        else:
            final_type = raw_type if raw_type in allowed_types else "product_issue"

        return {
            "status": final_status,
            "product_area": raw_output.get("product_area", "General Support"),
            "response": raw_output.get("response", "Information not found in the official support corpus."),
            "justification": raw_output.get("justification", "Automatic RAG-based analysis."),
            "request_type": final_type
        }
        
    except Exception as e:
        # High-resilience fallback for connection or parsing errors
        return {
            "status": "escalated",
            "product_area": "System Maintenance",
            "response": "We are currently experiencing technical difficulties. Your request has been escalated to a human agent.",
            "justification": f"System Error: {str(e)}",
            "request_type": "bug"
        }