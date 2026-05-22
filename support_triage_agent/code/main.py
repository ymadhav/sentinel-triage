import os
import sys

# --- PATH RESOLVER ---
# This ensures that 'src' is found even when running from the project root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

# Now we can safely import your modules
from src.knowledge_base import build_database
from src.pipeline import run_pipeline
from src.logger import init_logs  # Added for forensic trail

def main():
    print("========================================")
    print("   SENTINELTRIAGE: SECURE AI AGENT      ")
    print("========================================\n")
    
    # 1. Initialize Security Logs
    # This creates the data/logs folder automatically
    init_logs()
    
    # 2. Check if the Vector Database exists
    # Path is resolved relative to the 'code' folder
    vector_path = os.path.join(CURRENT_DIR, "vector_store")
    
    if not os.path.exists(vector_path):
        print("🚀 Vector store not found. Building database from corpus...")
        build_database()
    else:
        print("✅ Vector store found. System grounded and ready.\n")
    
    # 3. Start the Pipeline
    # This reads from support_tickets/ and writes to support_tickets/output.csv
    try:
        run_pipeline()
    except Exception as e:
        print(f"❌ CRITICAL ERROR in pipeline: {e}")

    print("\n========================================")
    print("PROCESS COMPLETE")
    print("Review: support_tickets/output.csv")
    print("Log: code/data/logs/security_audit.jsonl")
    print("========================================")

if __name__ == "__main__":
    main()