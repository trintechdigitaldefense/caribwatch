# Client Communication Playbook
## CaribWatch Continuous Visibility

---

## 1. Principles

- Speak in business impact, not technical jargon.
- Never claim “no threats exist” — only “no matching indicators observed in the period”.
- High-severity findings are communicated the same day.
- Medium findings are batched into the regular report unless the client requests otherwise.
- Always reference the authorization / ROE number.

---

## 2. Standard Messages

### A. First Deployment Confirmation

Subject: CaribWatch Visibility Service Active — [Client Name]

Body:
> CaribWatch continuous visibility is now active on the authorized systems under ROE reference [ROE-XXXX].
>
> We will monitor for matches against our Caribbean-focused indicator set and provide:
> - Immediate notification of High severity findings
> - Periodic summary reports (as agreed)
>
> Absence of alerts means no current indicators were matched — it does not guarantee the complete absence of all threats. Existing controls (antivirus, firewalls, MFA, etc.) remain essential.
>
> Primary contact: [Name] / [WhatsApp or email]

### B. High-Severity Alert

> **High-severity indicator match detected**
>
> Time (UTC): [timestamp]  
> Indicator: [domain/IP]  
> Type: [domain/ip]  
> Description: [plain language]  
> ROE Reference: [ROE-XXXX]
>
> Recommended immediate actions:
> 1. Confirm whether this traffic is expected.
> 2. If unexpected, isolate the affected system from the network if practical.
> 3. Contact us for deeper investigation support.
>
> We are standing by.

### C. Regular Summary (No High Findings)

> CaribWatch Summary — [Period]
>
> - High severity matches: 0
> - Medium severity matches: [N]
> - Low severity matches: [N]
>
> No high-severity indicators were observed. Medium items (if any) are listed in the attached report for your review. Full technical details available on request.
>
> Next scheduled report: [date]

### D. “No Findings” Clarification (use when client asks)

> No matching indicators were observed during the period. This is good news, but it does not mean the environment is free of all risk. CaribWatch only alerts on indicators present in its current intelligence set. Continue normal security hygiene and report any suspicious activity directly.

---

## 3. Escalation Path

| Severity | Client Notification | TrinTech Internal |
|----------|---------------------|-------------------|
| High | Same day (WhatsApp + email) | Lead analyst informed immediately |
| Medium | Next scheduled report (or sooner if volume spikes) | Logged and reviewed |
| Low | Included in report only | Logged |

---

## 4. Language to Avoid

- “You are secure” / “No threats found”
- “Guaranteed detection”
- Overly technical terms without explanation (C2, IOC, CIDR, etc.)
- Blame language toward the client

---

## 5. Handover / Offboarding Message

> As of [date], CaribWatch monitoring under ROE [ref] has ended. All local findings data will be securely deleted within 14 days unless you request a final export. Thank you for the engagement. We remain available for future visibility or assessment work.
