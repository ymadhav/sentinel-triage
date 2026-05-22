import json
import os
from datetime import datetime

# This ensures logs are stored inside code/data/logs so they get zipped for submission
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "logs")

def init_logs():
    """Creates the log directory if it doesn't exist."""
    os.makedirs(LOG_DIR, exist_ok=True)
    print(f"📁 Security Log Directory Initialized: {LOG_DIR}")

def log_security_event(event_type, details):
    """Appends a security event to the forensic JSONL log."""
    log_file = os.path.join(LOG_DIR, "security_audit.jsonl")
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "details": details
    }
    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")