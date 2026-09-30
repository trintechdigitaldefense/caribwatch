# Live Indicator Feed Maintenance Process

## Purpose
CaribWatch is only as good as its indicators. This document defines how TrinTech maintains a current, Caribbean-relevant indicator set.

---

## 1. Ownership

| Role | Responsibility |
|------|----------------|
| Primary (Jason / Lead Analyst) | Final approval of indicator additions/removals |
| Operator | Weekly refresh execution and documentation |
| Client Contact (when managed service) | Receives summary of material indicator changes |

---

## 2. Cadence

| Activity | Frequency |
|----------|-----------|
| Check TT-CSIRT advisories | Daily (or as published) |
| Review open-source / commercial feed deltas | At least weekly |
| Full indicator set review | Monthly |
| Emergency add (active campaign hitting T&T) | Same day |

---

## 3. Approved Sources (Priority Order)

1. **TT-CSIRT** official advisories — https://ttcsirt.gov.tt
2. Client-shared IOCs under NDA (incident response or threat intel sharing)
3. Reputable commercial threat intelligence feeds (if subscribed)
4. High-confidence open reports (Unit 42, Securelist, Mandiant, etc.) with clear Caribbean or LatAm relevance
5. Your own observed malicious infrastructure from engagements

Do **not** bulk-import unverified GitHub lists or low-reputation feeds.

---

## 4. Indicator Entry Standard

Every indicator added to `~/.caribwatch/intel/indicators.json` (or the managed feed) must have:

- `value` (domain, IP/CIDR, or user-agent)
- `severity` (`low` | `medium` | `high`)
- `desc` (plain-language reason)
- `tags` (array)
- `reference` (source advisory, report, or ticket)
- `added` (ISO date)
- `expires` (optional ISO date — default 90 days unless renewed)

Example:
```json
{
  "value": "example-phish.tt",
  "severity": "high",
  "desc": "Active e-Tax themed phishing domain reported by TT-CSIRT",
  "tags": ["phishing", "tt-local", "government-lure"],
  "reference": "TT-CSIRT-2026-XXX",
  "added": "2026-09-29",
  "expires": "2026-12-28"
}
```

---

## 5. Weekly Refresh Procedure

```bash
# 1. Backup current indicators
cp ~/.caribwatch/intel/indicators.json ~/.caribwatch/intel/indicators.json.bak.$(date +%Y%m%d)

# 2. Update from your maintained master copy or script
# (replace with your actual update method)

# 3. Validate JSON
python3 -m json.tool ~/.caribwatch/intel/indicators.json > /dev/null && echo "JSON OK"

# 4. Load into running instances
caribwatch update-intel

# 5. Record the change
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) - Weekly refresh - N indicators" >> ~/.caribwatch/logs/intel_changes.log
```

---

## 6. Removal / Expiry Rules

- Indicators past their `expires` date are removed or severity lowered unless renewed with fresh evidence.
- Indicators that generate repeated confirmed false positives are removed or retagged.
- Document every removal in the change log with reason.

---

## 7. Managed Service Note

When CaribWatch is run as a managed service for a client, TrinTech retains control of the indicator set. Material changes that significantly alter detection behaviour are noted in the next client report.
