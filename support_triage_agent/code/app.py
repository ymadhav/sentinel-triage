import streamlit as st
import pandas as pd
import os
import json
from src.pipeline import run_pipeline

# 1. Page Config & Professional Branding
st.set_page_config(page_title="SentinelTriage AI", page_icon="🛡️", layout="wide")

# Ensure folders exist
os.makedirs("data/input", exist_ok=True)
os.makedirs("data/output", exist_ok=True)
os.makedirs("data/logs", exist_ok=True)

st.title("🛡️ SentinelTriage: Secure AI Support Operations")
st.markdown("---")

# 2. Sidebar for System Management
with st.sidebar:
    st.header("Security Controls")
    if st.button("🔄 Reset System Cache"):
        files_to_remove = [
            "data/output/final_triage_results.csv",
            "data/input/support_tickets.csv",
            "data/logs/security_audit.jsonl"
        ]
        for f in files_to_remove:
            if os.path.exists(f):
                os.remove(f)
        st.success("All cache and logs cleared.")
    
    st.markdown("---")
    st.info("**System Status:** Local Llama 3.2 Active ✅")
    st.info("**Audit Layer:** Risk Scoring v2.0 Enabled 🛡️")

# 3. Data Ingestion Section
st.header("1. Secure Data Ingestion")
uploaded_file = st.file_uploader("Upload support_tickets.csv", type=['csv'])

if uploaded_file is not None:
    with open("data/input/support_tickets.csv", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("Data secured. Ready for analysis.")

    if st.button("🚀 Start Secure Triage Pipeline"):
        with st.spinner("Executing Cyber Audit & LLM Analysis..."):
            run_pipeline()
        st.balloons()
        st.success("Triage Complete!")

# 4. Display Results & Cyber Analytics
st.markdown("---")
st.header("2. Triage & Security Audit Analytics")

output_path = "data/output/final_triage_results.csv"

if os.path.exists(output_path):
    df = pd.read_csv(output_path)
    
    # --- ENHANCED CYBER METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Analyzed", len(df))
    with m2:
        # Highest risk score found in the batch
        max_risk = df['Risk_Score'].max() if 'Risk_Score' in df.columns else 0
        st.metric("Peak Risk Score", int(max_risk), delta="Critical" if max_risk >= 50 else None, delta_color="inverse")
    with m3:
        pii_count = len(df[df['Privacy_Status'] == 'Masked']) if 'Privacy_Status' in df.columns else 0
        st.metric("PII Redacted", pii_count)
    with m4:
        # Count only Critical and High severity escalations
        critical_alerts = len(df[df['Severity'].isin(['Critical', 'High'])]) if 'Severity' in df.columns else 0
        st.metric("Security Alerts", critical_alerts)

    # --- ADVANCED VISUALIZATIONS ---
    st.markdown("### 📊 Threat Landscape")
    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        st.write("**Risk Distribution by Company**")
        if 'Company' in df.columns and 'Risk_Score' in df.columns:
            risk_chart = df.groupby('Company')['Risk_Score'].sum()
            st.bar_chart(risk_chart)

    with viz_col2:
        st.write("**Severity Breakdown**")
        if 'Severity' in df.columns:
            sev_chart = df['Severity'].value_counts()
            st.bar_chart(sev_chart)

    # --- GRANULAR ROW HIGHLIGHTING ---
    def highlight_severity(row):
        # Professional color coding based on Severity level
        if row.get('Severity') == 'Critical':
            return ['background-color: #fce4e4; color: #cc0000; font-weight: bold'] * len(row)
        if row.get('Severity') == 'High':
            return ['background-color: #fff0e6; color: #e65c00'] * len(row)
        if row.get('Privacy_Status') == 'Masked':
            return ['background-color: #fff9db'] * len(row)
        return [''] * len(row)

    st.subheader("Secure Analysis Breakdown")
    st.dataframe(
        df.style.apply(highlight_severity, axis=1),
        use_container_width=True
    )
    
    # 5. Export Report
    st.download_button(
        label="📥 Download Full Security Audit (CSV)",
        data=df.to_csv(index=False),
        file_name="sentinel_audit_report.csv",
        mime="text/csv"
    )

    # --- 6. FORENSIC AUDIT TRAIL ---
    st.markdown("---")
    st.header("3. 📜 Security Forensics (Audit Trail)")
    log_file = "data/logs/security_audit.jsonl"
    
    if os.path.exists(log_file):
        with st.expander("View Immutable System Logs"):
            with open(log_file, "r") as f:
                logs = [json.loads(line) for line in f.readlines()]
                log_df = pd.DataFrame(logs).sort_values(by="timestamp", ascending=False)
                st.table(log_df.head(15))
            
            with open(log_file, "rb") as f:
                st.download_button("📁 Download Audit Trail (.jsonl)", f, "forensic_log.jsonl")
    else:
        st.info("No security events logged yet.")

else:
    st.info("Awaiting input. Please upload a CSV and run the pipeline.")