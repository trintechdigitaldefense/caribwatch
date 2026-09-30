# CaribWatch v0.2.2

**Caribbean-Specific Threat Visibility Tool**  
Built by [TrinTech Digital Defense](https://trintechdigitaldefense.github.io/)

CaribWatch provides continuous, lightweight threat visibility for Trinidad & Tobago and Caribbean SMBs that do not operate a SOC or SIEM.

## Current Status

**v0.2.2** is operationally complete for careful pilot use. All previously identified remaining items are now documented:

| Item | Document |
|------|----------|
| Live indicator maintenance process | [docs/LIVE_INTEL_PROCESS.md](docs/LIVE_INTEL_PROCESS.md) |
| Validation (lab + realistic traffic) | [docs/VALIDATION_GUIDE.md](docs/VALIDATION_GUIDE.md) |
| Rules of Engagement template | [docs/RULES_OF_ENGAGEMENT.md](docs/RULES_OF_ENGAGEMENT.md) |
| False-positive tuning | [docs/FALSE_POSITIVE_TUNING.md](docs/FALSE_POSITIVE_TUNING.md) |
| Client communication playbook | [docs/CLIENT_COMMUNICATION_PLAYBOOK.md](docs/CLIENT_COMMUNICATION_PLAYBOOK.md) |
| Backup & recovery | [docs/BACKUP_AND_RECOVERY.md](docs/BACKUP_AND_RECOVERY.md) |
| Update mechanism | [docs/UPDATE_MECHANISM.md](docs/UPDATE_MECHANISM.md) |

**Before any paying client production deployment you must still:**
1. Maintain a real, current indicator feed (process defined)
2. Complete validation on staging/realistic traffic
3. Sign an ROE with the client

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

## Documentation Index

- [Rules of Engagement](docs/RULES_OF_ENGAGEMENT.md)
- [Validation Guide](docs/VALIDATION_GUIDE.md)
- [Live Intel Process](docs/LIVE_INTEL_PROCESS.md)
- [False Positive Tuning](docs/FALSE_POSITIVE_TUNING.md)
- [Client Communication Playbook](docs/CLIENT_COMMUNICATION_PLAYBOOK.md)
- [Backup & Recovery](docs/BACKUP_AND_RECOVERY.md)
- [Update Mechanism](docs/UPDATE_MECHANISM.md)

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
