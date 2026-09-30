# CaribWatch Validation Guide

## Purpose

Before using CaribWatch on any client network, validate that it behaves correctly in a controlled environment. This guide covers practical validation steps.

---

## 1. Lab Validation Checklist

### A. Clean Baseline
1. Deploy CaribWatch on a clean Linux host (or VM) with no known malicious traffic.
2. Run:
   ```bash
   caribwatch init --org "Lab Test" --auth-ref LAB-001
   caribwatch update-intel
   caribwatch scan
   caribwatch status
   ```
3. Expected result: zero or near-zero findings (only if your indicator set contains ranges that legitimately overlap normal traffic).

### B. Positive Control (Known Indicator)
1. Temporarily add a test indicator you control (e.g., a domain or IP you own) to `~/.caribwatch/intel/indicators.json`.
2. Generate traffic to that indicator (e.g., `curl http://your-test-domain` or connect to a test IP).
3. Run `caribwatch scan`.
4. Confirm the indicator is detected at the correct severity and appears in the report.
5. Remove the test indicator after validation.

### C. CIDR Matching
1. Confirm an IP that falls inside a configured CIDR (e.g., `185.220.101.10` against `185.220.101.0/24`) is correctly matched.
2. Confirm an IP just outside the range is **not** matched.

### D. Private IP Suppression
1. With `suppress_private_ips: true` (default), confirm RFC1918 addresses do not generate alerts.
2. Temporarily set to `false` and confirm private IPs can be matched if desired.

### E. Alert Cooldown
1. Trigger the same indicator twice within the cooldown window.
2. Confirm the second alert is suppressed.

### F. Authorization Logging
1. Run scans with and without `--force`.
2. Confirm authorization reference is recorded.

### G. Client Report Format
```bash
caribwatch report --daily --client
```
Review the generated Markdown for clarity suitable for non-technical stakeholders.

---

## 2. Realistic Traffic Validation

Perform these steps on a staging network that mirrors the client environment as closely as possible:

- Same operating system and privilege level
- Similar outbound internet patterns
- Presence of common business applications
- Presence of any residential / mobile devices if applicable

Run CaribWatch in `monitor` mode for at least 24–48 hours. Review:

- Volume of observations per scan
- False positive rate
- Whether high-severity items are actionable
- Resource usage (CPU / memory)

Document any tuning required (see `FALSE_POSITIVE_TUNING.md`).

---

## 3. Indicator Quality Gate

Before client deployment:

- [ ] Placeholder / example indicators replaced with current, verified sources
- [ ] Each indicator has severity, description, and reference
- [ ] No overly broad ranges that will flood alerts
- [ ] Process exists to refresh indicators (see `LIVE_INTEL_PROCESS.md`)

---

## 4. Final Sign-off

Validation performed by: _______________  
Date: _______________  
Environment: _______________  
Result: Pass / Pass with notes / Fail  
Notes: _______________________________________________

Only after a formal Pass (or Pass with documented tuning) should CaribWatch be deployed under a signed Rules of Engagement.
