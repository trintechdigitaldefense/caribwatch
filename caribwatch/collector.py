import socket
from typing import List, Dict, Any

try:
    import psutil
except ImportError:
    psutil = None


def collect_network_observations() -> List[Dict[str, str]]:
    """
    Collect basic network observations from the local system.
    Returns a list of {type, value} dicts that can be matched against intel.
    """
    observations = []

    if psutil is None:
        return observations

    # Active connections
    try:
        for conn in psutil.net_connections(kind="inet"):
            if conn.raddr:
                remote_ip = conn.raddr.ip
                observations.append({"type": "ip", "value": remote_ip})

                # Attempt reverse DNS (best effort, non-blocking style)
                try:
                    hostname = socket.gethostbyaddr(remote_ip)[0]
                    if hostname:
                        observations.append({"type": "domain", "value": hostname})
                except (socket.herror, socket.gaierror, OSError):
                    pass
    except (psutil.AccessDenied, PermissionError):
        # Running without sufficient privileges
        pass

    # Listening addresses (less useful for threat intel but included)
    try:
        for conn in psutil.net_connections(kind="inet"):
            if conn.status == "LISTEN" and conn.laddr:
                observations.append({"type": "ip", "value": conn.laddr.ip})
    except (psutil.AccessDenied, PermissionError):
        pass

    # Deduplicate
    seen = set()
    unique = []
    for obs in observations:
        key = (obs["type"], obs["value"])
        if key not in seen:
            seen.add(key)
            unique.append(obs)

    return unique


def collect_process_network_hints() -> List[Dict[str, Any]]:
    """
    Lightweight process + connection summary for reporting.
    """
    if psutil is None:
        return []

    hints = []
    try:
        for proc in psutil.process_iter(["pid", "name", "username"]):
            try:
                conns = proc.connections(kind="inet")
                if conns:
                    remote_ips = list({c.raddr.ip for c in conns if c.raddr})
                    if remote_ips:
                        hints.append({
                            "pid": proc.info["pid"],
                            "name": proc.info["name"],
                            "user": proc.info.get("username"),
                            "remote_ips": remote_ips[:5],  # limit
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception:
        pass

    return hints
