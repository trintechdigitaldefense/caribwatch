# CaribWatch v0.2

**Caribbean-Specific Threat Visibility Tool**  
Built by [TrinTech Digital Defense](https://trintechdigitaldefense.github.io/)

CaribWatch provides continuous, lightweight threat visibility for Trinidad & Tobago and Caribbean SMBs that do not operate a SOC or SIEM.

It focuses on regional threats:
- Residential proxy / botnet exit-node indicators
- Local phishing and WhatsApp/SMS lure domains
- Illegal streaming and cracked-software malware signals
- Suspicious outbound network behavior

## Status

**v0.2.0** — Hardened MVP suitable for controlled internal use and limited pilot deployments.  
Still requires real Caribbean threat intelligence before broad client production use.

## What's New in v0.2

- CIDR / IP-range matching
- Improved network visibility and privilege handling
- Structured authorization logging
- Cleaner client-facing Markdown + HTML reports
- Better error handling and resource limits
- Configurable false-positive suppression
- Severity thresholding and alert cooldown
- Clear separation of operator vs client report modes

## Installation

```bash
git clone https://github.com/trintechdigitaldefense/caribwatch.git
cd caribwatch
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```bash
caribwatch init
caribwatch update-intel
caribwatch scan
caribwatch monitor
caribwatch report --daily --client
caribwatch status
```

## Authorized Use Only

This tool is for authorized defensive monitoring only.  
Unauthorized use may violate the Trinidad and Tobago Cybercrimes Act and equivalent laws.

Always obtain written authorization before monitoring any network you do not own.

## Contact

TrinTech Digital Defense  
Email: trintechdigitaldefense@gmail.com  
WhatsApp: +1-868-362-0679  
Website: https://trintechdigitaldefense.github.io/

---

Built in Trinidad & Tobago for the Caribbean.
