# CaribWatch Update Mechanism

## Goal
Push new versions of CaribWatch to client or internal hosts safely, with minimal downtime and clear rollback.

---

## 1. Versioning

We follow simple semantic versioning visible in the package and `caribwatch --version`:

- **0.2.x** — current hardened MVP line
- Breaking changes will bump the minor or major version and be called out in release notes

---

## 2. Standard Update Procedure (Self-Hosted / Client Host)

```bash
# 1. Stop monitor if running
# (Ctrl+C or systemctl stop caribwatch if you created a service)

# 2. Backup current state
tar -czf ~/caribwatch-pre-update-$(date +%Y%m%d).tar.gz -C $HOME .caribwatch

# 3. Pull latest code
cd /path/to/caribwatch
git fetch --tags
git checkout main          # or a specific tag e.g. v0.2.2
git pull

# 4. Re-install
pip install -r requirements.txt
pip install -e .

# 5. Verify
caribwatch --version
caribwatch status

# 6. Resume monitoring
caribwatch monitor
```

---

## 3. Recommended: systemd Service (Optional but Cleaner)

Create `/etc/systemd/system/caribwatch.service`:

```ini
[Unit]
Description=CaribWatch Continuous Visibility
After=network.target

[Service]
Type=simple
User=caribwatch          # or the appropriate service user
WorkingDirectory=/opt/caribwatch
ExecStart=/usr/local/bin/caribwatch monitor --interval 300
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now caribwatch
sudo systemctl status caribwatch
```

Updates become:

```bash
sudo systemctl stop caribwatch
# perform git pull + pip install
sudo systemctl start caribwatch
```

---

## 4. Managed Service Update Flow (TrinTech Operated)

1. Test new version on internal lab host.
2. Announce maintenance window to client if the update is material.
3. Backup client findings DB.
4. Deploy update.
5. Verify with `caribwatch status` and a short monitor run.
6. Note the version change in the next client report.

---

## 5. Rollback

If a new version misbehaves:

```bash
cd /path/to/caribwatch
git checkout <previous-tag-or-commit>
pip install -e .
# restore config/findings from the pre-update tarball if needed
caribwatch status
```

---

## 6. Notification of Material Changes

Material changes (detection logic, new required config keys, report format changes) are documented in the GitHub release notes and, for managed clients, summarised in the next scheduled report.
