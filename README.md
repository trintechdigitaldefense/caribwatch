# CaribWatch v0.2.1

**Caribbean-Specific Threat Visibility Tool**  
Built by [TrinTech Digital Defense](https://trintechdigitaldefense.github.io/)

CaribWatch provides continuous, lightweight threat visibility for Trinidad & Tobago and Caribbean SMBs that do not operate a SOC or SIEM.

## Current Status

**v0.2.1** — Hardened tool with:
- Publicly documented example indicators (TT-CSIRT, published malware reports)
- CIDR matching, alert cooldown, privilege checks
- Client-facing report mode
- Formal Rules of Engagement template
- Validation guide

**Still required before broad production client use:**
1. Replace example indicators with your maintained, current feed
2. Complete lab + realistic traffic validation (see `docs/VALIDATION_GUIDE.md`)
3. Sign a Rules of Engagement with each client (template in `docs/RULES_OF_ENGAGEMENT.md`)

## Installation

```bash
git clone https://github.com/trintechdigitaldefense/caribwatch.git
cd caribwatch
pip install -r requirements.txt
pip install -e .
```

## Quick Start

```bash
caribwatch init --org "Client Name" --auth-ref ROE-2026-001
caribwatch update-intel
caribwatch scan
caribwatch monitor
caribwatch report --daily --client
caribwatch status
```

## Documentation

- [Rules of Engagement Template](docs/RULES_OF_ENGAGEMENT.md)
- [Validation Guide](docs/VALIDATION_GUIDE.md)

## Authorized Use Only

This tool is for authorized defensive monitoring only.  
Unauthorized use may violate the Trinidad and Tobago Cybercrimes Act and equivalent laws.

Always obtain written authorization (signed ROE) before monitoring any network you do not own.

## Contact

TrinTech Digital Defense  
Email: trintechdigitaldefense@gmail.com  
WhatsApp: +1-868-362-0679  
Website: https://trintechdigitaldefense.github.io/

---

Built in Trinidad & Tobago for the Caribbean.
