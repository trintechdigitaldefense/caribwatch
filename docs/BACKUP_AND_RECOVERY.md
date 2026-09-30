# Backup & Recovery — CaribWatch Findings

## What Must Be Protected

| Path | Content | Criticality |
|------|---------|-------------|
| `~/.caribwatch/findings.db` | All findings + scan history + auth log | High |
| `~/.caribwatch/intel/indicators.json` | Current indicator set | High |
| `~/.caribwatch/config.json` | Runtime configuration | Medium |
| `~/.caribwatch/reports/` | Generated reports | Medium |
| `~/.caribwatch/logs/` | Change and operational logs | Low–Medium |

---

## 1. Recommended Backup Method (Simple & Reliable)

### Daily cron (Linux)

```bash
# Edit crontab
crontab -e

# Add (runs 02:15 daily)
15 2 * * * tar -czf /var/backups/caribwatch-$(date +\%Y\%m\%d).tar.gz -C $HOME .caribwatch && find /var/backups -name 'caribwatch-*.tar.gz' -mtime +14 -delete
```

Adjust the backup destination to a location that is itself backed up (external disk, object storage, or client-approved share).

### Manual one-liner

```bash
tar -czf caribwatch-backup-$(date +%Y%m%d).tar.gz -C $HOME .caribwatch
```

---

## 2. Managed Service Option

When TrinTech runs CaribWatch for a client:

- Findings DB is backed up daily to TrinTech-controlled storage under the client’s engagement folder.
- Retention follows the ROE (default 30 days active, longer if required by the engagement).
- Client may request an export of findings at any time during the engagement.

---

## 3. Recovery Procedure

1. Stop any running `caribwatch monitor` process.
2. Restore the tarball:
   ```bash
   tar -xzf caribwatch-backup-YYYYMMDD.tar.gz -C $HOME
   ```
3. Verify:
   ```bash
   caribwatch status
   caribwatch report --hours 24
   ```
4. Resume monitoring if required.

---

## 4. Integrity Check

After restore, optionally verify the SQLite database:

```bash
sqlite3 ~/.caribwatch/findings.db "PRAGMA integrity_check;"
```

Expected output: `ok`

---

## 5. Offboarding / Secure Deletion

Per ROE, on termination:

```bash
# Final export if requested by client
tar -czf FINAL-caribwatch-export-$(date +%Y%m%d).tar.gz -C $HOME .caribwatch

# Secure deletion (example)
shred -u ~/.caribwatch/findings.db 2>/dev/null || rm -f ~/.caribwatch/findings.db
rm -rf ~/.caribwatch
```

Document the deletion date and method in the engagement close-out notes.
