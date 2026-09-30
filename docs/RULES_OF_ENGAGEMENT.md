# Rules of Engagement (ROE)
## CaribWatch Continuous Visibility Service
### TrinTech Digital Defense

**Document Version:** 1.0  
**Effective Date:** _______________  
**Client / Organization:** _______________  
**Authorization Reference:** _______________  

---

## 1. Purpose

This Rules of Engagement defines the authorized scope, limitations, responsibilities, and conditions under which TrinTech Digital Defense ("Provider") may deploy and operate the CaribWatch continuous threat visibility tool on systems and networks belonging to the Client.

CaribWatch is a defensive monitoring tool. It is not an offensive security assessment, penetration test, or red-team exercise.

---

## 2. Authorization

2.1 The Client confirms it owns or has explicit legal authority to authorize monitoring of the systems and network segments listed in **Appendix A – In-Scope Assets**.

2.2 The Client grants TrinTech Digital Defense written authorization to:
- Install and run CaribWatch on designated host(s)
- Collect network connection metadata and related observations
- Match observations against threat indicators
- Generate alerts and reports
- Retain findings for the duration specified in this ROE

2.3 This authorization is limited to defensive monitoring only. No exploitation, vulnerability scanning, password guessing, social engineering, or active attack simulation is authorized under this ROE.

---

## 3. Scope

### In Scope
- Network connection metadata (remote IPs, ports, reverse DNS where available)
- Matching against the configured indicator set
- Generation of operator and client-facing reports
- Optional webhook / alerting to Client-designated channels

### Explicitly Out of Scope
- Deep packet inspection or content inspection of traffic
- Endpoint process memory analysis or disk forensics (unless separately authorized)
- Active scanning, port scanning, or vulnerability exploitation
- Monitoring of networks or systems not listed in Appendix A
- Any action that modifies, disrupts, or degrades Client systems

---

## 4. Duration

- Start Date: _______________
- End Date / Review Date: _______________
- This ROE may be extended only by written agreement of both parties.

---

## 5. Data Handling & Retention

5.1 Findings and logs are stored locally on the monitored host under `~/.caribwatch/` unless a Client-approved remote destination is configured.

5.2 Default retention: 30 days (configurable).

5.3 TrinTech will not transfer findings to third parties except as required by law or with prior written Client consent.

5.4 Upon termination, TrinTech will securely delete retained data within 14 days unless otherwise agreed in writing.

---

## 6. Responsibilities

**Client**
- Provide accurate in-scope asset list
- Ensure necessary privileges for CaribWatch to operate
- Designate primary technical contact
- Review alerts and reports in a timely manner
- Maintain its own legal authorization for the monitored environment

**TrinTech Digital Defense**
- Operate CaribWatch only within the authorized scope
- Maintain professional confidentiality (NDA applies)
- Provide clear, non-technical summaries when requested
- Notify Client promptly of high-severity findings
- Document all authorization references in tool logs

---

## 7. Limitations & Disclaimer

7.1 CaribWatch detects matches against its configured indicator set. Absence of alerts does not guarantee the absence of threats.

7.2 Indicator quality depends on the feed in use. Client and Provider share responsibility for keeping indicators current.

7.3 TrinTech is not liable for false positives, false negatives, or decisions made solely on the basis of CaribWatch output.

7.4 This service does not replace antivirus, EDR, firewalls, or other security controls.

---

## 8. Legal Compliance

Both parties acknowledge that activities must comply with the laws of Trinidad and Tobago, including the Cybercrimes Act, and any other applicable jurisdiction. Unauthorized monitoring is prohibited.

---

## 9. Signatures

**For the Client**

Name: _______________________________  
Title: _______________________________  
Signature: ____________________________  
Date: ________________________________

**For TrinTech Digital Defense**

Name: _______________________________  
Title: _______________________________  
Signature: ____________________________  
Date: ________________________________

---

## Appendix A – In-Scope Assets

| Asset / Network Segment | Description | Notes |
|-------------------------|-------------|-------|
| | | |
| | | |
| | | |

---

## Appendix B – Contacts

| Role | Name | Email / Phone |
|------|------|---------------|
| Client Primary Technical Contact | | |
| Client Escalation | | |
| TrinTech Primary | | trintechdigitaldefense@gmail.com / +1-868-362-0679 |
| TrinTech Escalation | | |

---

**TrinTech Digital Defense**  
Trinidad & Tobago  
https://trintechdigitaldefense.github.io/
