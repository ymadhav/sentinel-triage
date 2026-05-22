# sentinel-triage
# 🛡️ SentinelTriage AI: Secure Multi-Domain Support Agent

[![Live Demo](https://img.shields.io/badge/Live_Demo-Hugging_Face-yellow)](https://huggingface.co/spaces/sudhanshu78/sentinel-triage-ai)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![Groq API](https://img.shields.io/badge/Powered_by-Groq_Llama_3.3-orange.svg)](https://groq.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)

SentinelTriage AI is an enterprise-grade support triage system built for the **HackerRank Orchestrate Hackathon**. It uses the ultra-fast **Groq API (Llama 3.3 70B)** to categorize, answer, and audit support tickets for **HackerRank**, **Claude**, and **Visa**, while ensuring total data privacy through a secure pipeline architecture.

---

## 🌟 Key Innovation: The Cyber Audit Layer
Unlike standard AI agents, SentinelTriage includes a **Security-First Audit Layer** that acts as a gatekeeper:
- **Redacts PII:** Automatically masks Emails and IP addresses *before* they reach the LLM.
- **Risk Scoring:** Assigns a mathematical "Risk Score" to every ticket.
- **Threat Detection:** Detects keywords like "hack" or "breach" and escalates them directly to a Security Officer, bypassing the AI entirely.

---

## 🚀 Live Demo
**Try the live application here:** [SentinelTriage on Hugging Face Spaces](https://huggingface.co/spaces/sudhanshu78/sentinel-triage-ai)

*(Note: The live demo is powered by the Groq API, allowing for sub-second inference speeds per ticket).*

---

## 🏗️ System Architecture & Features

This project moves beyond standard LLM wrappers by implementing a resilient, multi-layered pipeline:

1. **Self-Healing Vector Database:** Utilizes a persistent ChromaDB instance. If the container resets, the database automatically rebuilds the vector space using the local support corpus.
2. **Context-Grounded RAG:** Uses `all-MiniLM-L6-v2` embeddings to search the support corpus, ensuring the AI agent only answers based on verified company policies.
3. **Schema-Strict JSON Enforcement:** The LLM is forced via prompt engineering and Groq's JSON mode to return structured data mapping perfectly to the required Hackathon grading schema.
4. **High-Speed Inference:** Migrated from local CPU inference to the **Groq API** to reduce processing time from ~45 seconds/ticket to under ~1 second/ticket.

---

## 📋 Prerequisites
Before you start, ensure you have the following installed:
1. **Python 3.10 or higher**
2. **A Free Groq API Key** (Get one at [console.groq.com](https://console.groq.com/))

---

## 🛠️ Installation & Setup

### Step 1: Clone and Navigate
Open your terminal (or PowerShell) in the project root folder:
```bash
git clone [https://github.com/yourusername/sentinel-triage.git](https://github.com/yourusername/sentinel-triage.git)
cd sentinel-triage

```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
python -m venv venv
# On Mac/Linux:
source venv/bin/activate  
# On Windows:
.\venv\Scripts\activate

```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt

```

### Step 4: Set API Key

Export your Groq API key to your environment variables:

```bash
# On Mac/Linux:
export GROQ_API_KEY="your_api_key_here"  
# On Windows:
set GROQ_API_KEY="your_api_key_here"

```

---

## 🚀 How to Run the System

### Option 1: Streamlit Dashboard (Interactive Analytics)

View the risk scores, PII redaction metrics, and the forensic audit trail in a professional UI.

```bash
streamlit run code/app.py

```

*Navigate to `http://localhost:8501` in your browser.*

### Option 2: Terminal CLI (Official Submission Mode)

This mode processes the official tickets and generates the `output.csv` required for the hackathon grading.

```bash
python code/main.py

```

---

## 📊 Expected Output Schema

The AI agent is engineered to output structured analytics for every ticket:

* `status`: 'replied' or 'escalated'
* `product_area`: Domain of the issue (e.g., Billing, Account Access)
* `response`: User-facing answer grounded in the database
* `justification`: AI reasoning
* `request_type`: product_issue, feature_request, bug, or invalid

---

## 📁 Project Structure

```text
sentinel-triage/
├── data/                    # Vector database and official support corpus
├── support_tickets/         # Official inputs and final output.csv
└── code/                    # Application Source Code
    ├── main.py              # CLI Entry point
    ├── app.py               # Streamlit Analytics Dashboard
    ├── src/                 # Modular logic (Audit, Groq LLM Agent, Knowledge Base)
    └── data/logs/           # Forensic security logs

```

---

## ✅ Verification Checklist

To confirm the system is working perfectly locally:

1. **Check Speed:** Ensure the Groq API is processing tickets in under 1 second.
2. **Check Privacy:** Add a ticket with an email to the input CSV; verify the output shows `[EMAIL_REDACTED]`.
3. **Check Security:** Add a ticket with the word "hack"; verify it is automatically `escalated` with a `Critical` severity.

---

## 👨‍💻 Author

**Sudhanshu Yadav**

* [LinkedIn](www.linkedin.com/in/sudhanshu0)
* B.Sc. AI & ML @ Sharda University

*Built for HackerRank Orchestrate 2026.*

```
