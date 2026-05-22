import re

class CyberAudit:
    def __init__(self):
        self.pii_patterns = {
            "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "IP": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        self.critical_threats = ["hack", "breach", "malware", "leak"]

    def scan_ticket(self, text):
        findings = []
        masked_text = text
        risk_score = 0
        
        for label, pattern in self.pii_patterns.items():
            if re.search(pattern, text):
                findings.append(f"PII: {label}")
                risk_score += 15
                masked_text = re.sub(pattern, f"[{label}_REDACTED]", masked_text)

        for word in self.critical_threats:
            if re.search(rf'\b{word}\b', text.lower()):
                findings.append(f"CRITICAL: {word}")
                risk_score += 50

        return {
            "masked_text": masked_text,
            "security_flag": risk_score >= 50,
            "severity": "Critical" if risk_score >= 50 else ("High" if risk_score >= 15 else "Low"),
            "risk_score": risk_score,
            "findings": ", ".join(findings) if findings else "Clean"
        }