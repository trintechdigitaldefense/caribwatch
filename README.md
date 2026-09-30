# CaribWatch

**Caribbean-Specific Threat Visibility Tool**  
Built by [TrinTech Digital Defense](https://trintechdigitaldefense.github.io/)

CaribWatch is a lightweight, continuous threat visibility tool designed for Trinidad & Tobago and Caribbean SMBs that do not have a SOC or SIEM.

It focuses on the threats that actually hit the region:

- Residential proxy / botnet exit-node indicators
- Local phishing and WhatsApp/SMS lure domains
- Illegal streaming and cracked-software malware distribution signals
- Suspicious outbound network behavior

## Why CaribWatch?

Most security tools are built for enterprise environments. Caribbean businesses need something that:

- Runs on modest hardware or a small VPS
- Requires almost no configuration
- Produces clear, actionable alerts instead of noise
- Understands regional threat patterns

## Features (MVP)

- One-shot and continuous monitoring modes
- Curated indicator matching (domains, IPs, user-agents)
- Simple severity scoring
- Console + JSON + optional webhook alerts
- Daily / on-demand summary reports
- Fully local by default (nothing leaves the machine unless you configure a webhook)

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
caribwatch monitor          # continuous mode
caribwatch report --daily
caribwatch status
```

## Authorized Use Only

This tool is intended for authorized defensive monitoring of systems you own or have explicit written permission to monitor.

Unauthorized use may violate the Trinidad and Tobago Cybercrimes Act and equivalent laws in other jurisdictions.

## Contact

TrinTech Digital Defense  
Email: trintechdigitaldefense@gmail.com  
WhatsApp: +1-868-362-0679  
Website: https://trintechdigitaldefense.github.io/

---

Built in Trinidad & Tobago for the Caribbean.
