import pandas as pd
import os
from src.llm_agent import triage_ticket
from src.cyber_audit import CyberAudit
from src.logger import log_security_event

# --- PATH RESOLUTION FOR OFFICIAL REPO STRUCTURE ---
# Current File: code/src/pipeline.py
CODE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # points to /code
ROOT_DIR = os.path.dirname(CODE_DIR)                                   # points to / (project root)

# Official Hackathon Paths
INPUT_FILE = os.path.join(ROOT_DIR, "support_tickets", "support_tickets.csv")
FINAL_OUTPUT = os.path.join(ROOT_DIR, "support_tickets", "output.csv")

def run_pipeline():
    print("==========================================")
    print("   SENTINELTRIAGE: OFFICIAL PIPELINE      ")
    print("==========================================\n")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ ERROR: Official input file not found at {INPUT_FILE}")
        return
    
    # Initialize the Enhanced Cyber Audit layer
    audit = CyberAudit()
    
    # Load official tickets. fillna("None") to handle empty fields safely
    df = pd.read_csv(INPUT_FILE).fillna("None")
    results = []
    
    total_tickets = len(df)
    print(f"📊 Processing {total_tickets} tickets. Generating official output...\n")
    
    for index, row in df.iterrows():
        # Map official schema fields (handling both lowercase and capitalized headers)
        issue = str(row.get('issue', row.get('Issue', '')))
        subject = str(row.get('subject', row.get('Subject', '')))
        company = str(row.get('company', row.get('Company', 'None')))
        
        try:
            # 1. Run Enhanced Cyber Audit
            audit_result = audit.scan_ticket(issue)
            
            # --- Forensic Logging ---
            if audit_result['risk_score'] > 0:
                event_type = "SECURITY_ALERT" if audit_result['security_flag'] else "PRIVACY_MASKING"
                log_security_event(event_type, {
                    "company": company,
                    "severity": audit_result['severity'],
                    "risk_score": audit_result['risk_score'],
                    "findings": audit_result['findings']
                })

            # 2. Decision Logic: Security Center vs AI Agent
            if audit_result['security_flag']:
                triage_data = {
                    "status": "escalated",
                    "product_area": "Cyber Security",
                    "response": f"SECURITY ALERT: {audit_result['severity']} risk detected. Routing to security operations.",
                    "justification": f"Automated Security Flag: {audit_result['findings']}",
                    "request_type": "invalid" # Mapped to official allowed value
                }
            else:
                # Send MASKED text to AI
                triage_data = triage_ticket(audit_result['masked_text'], subject, company)
            
            # 3. BUILD ROW (Aligned with Official Schema + Your Metrics)
            # The first 5 keys are the official requirements. The rest are for your Dashboard.
            full_row = {
                "status": str(triage_data.get("status", "escalated")).lower(),
                "product_area": triage_data.get("product_area", "General"),
                "response": triage_data.get("response", "N/A"),
                "justification": triage_data.get("justification", "Processed via local RAG."),
                "request_type": str(triage_data.get("request_type", "product_issue")).lower(),
                
                # --- Extended Analytics (Keeps your Dashboard working) ---
                "Audit_Findings": audit_result['findings'],
                "Severity": audit_result['severity'],
                "Risk_Score": audit_result['risk_score'],
                "Privacy_Status": "Masked" if "REDACTED" in audit_result['masked_text'] else "Clean",
                "Original_Company": company
            }
            results.append(full_row)
            
            print(f"✅ [{index + 1}/{total_tickets}] Analyzed: {company}")
            
        except Exception as e:
            print(f"⚠️ Error processing row {index}: {e}")
            continue

    # Save to official location
    os.makedirs(os.path.dirname(FINAL_OUTPUT), exist_ok=True)
    pd.DataFrame(results).to_csv(FINAL_OUTPUT, index=False)
    
    print("\n✨ PIPELINE COMPLETE!")
    print(f"📂 Official Predictions: {FINAL_OUTPUT}")
    print("==========================================")