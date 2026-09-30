# False Positive Tuning Guide

## Reality
Every environment produces some noise. The goal is not zero alerts — it is **high-signal alerts** that a human can act on.

---

## 1. Common Sources of False Positives

| Source | Why it happens | Mitigation |
|--------|----------------|------------|
| Broad proxy/Tor CIDRs | Legitimate users or services exit via these ranges | Raise severity threshold or exclude specific client-known ranges |
| Business partner IPs that overlap threat ranges | Shared hosting or previous compromise | Add to local allow-list |
| Reverse DNS that partially matches a bad domain | Weak string matching | Prefer exact domain matches; avoid partial matching for domains |
| High volume of medium findings | Threshold set too low | Set `alert_threshold` to `high` for noisy environments |
| Repeated alerts for same indicator | Cooldown too short | Increase `alert_cooldown_seconds` |

---

## 2. Tuning Levers (in order of preference)

1. **Improve indicator quality** (remove stale or overly broad entries)
2. **Raise alert threshold** (`alert_threshold: "high"`)
3. **Increase cooldown** (`alert_cooldown_seconds`)
4. **Enable private IP suppression** (already default)
5. **Local allow-list** (see below)
6. **Reduce scan frequency** only as last resort

---

## 3. Local Allow-List (Recommended Pattern)

Create `~/.caribwatch/intel/allowlist.json`:

```json
{
  "domains": ["trusted-partner.example.com"],
  "ips": ["203.0.113.0/24"],
  "notes": "Client-approved exceptions — reviewed YYYY-MM-DD"
}
```

Future versions of CaribWatch will load this file automatically. Until then, remove or comment conflicting indicators manually and document the exception.

---

## 4. Tuning Workflow After First 48 Hours

1. Run `caribwatch report --hours 48`
2. For every Medium/High finding ask:
   - Is this expected business traffic?
   - Is the indicator still valid?
   - Can we safely exclude or lower severity?
3. Apply changes and re-run for another 24 hours.
4. Document final tuning decisions in the client folder / ticket.

---

## 5. When to Escalate Instead of Tuning

- High-severity match on a domain/IP with fresh TT-CSIRT or commercial confirmation
- Same indicator appearing across multiple client hosts
- Indicator tied to active ransomware, banking trojan, or credential theft campaign

Do not tune away real threats.
