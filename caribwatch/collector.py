import socket
from typing import List, Dict, Any

try:
    import psutil
except ImportError:
    psutil = None


def collect_network_observations(max_observations: int = 5000) -> List[Dict[str, str]]:
    """
    Collect network observations with basic privilege and resource protection.
    Returns list of {type, value} dicts.
    """
    observations: List[Dict[str, str]] = []

    if psutil is None:
        return observations

    seen = set()

    def add(obs_type: str, value: str):
        if len(observations) >= max_observations:
            return
        key = (obs_type, value)
        if key not in seen and value:
            seen.add(key)
            observations.append({"type": obs_type, "value": value})

    # Active connections
    try:
        for conn in psutil.net_connections(kind="inet"):
            if conn.raddr:
                remote_ip = str(conn.raddr.ip)
                add("ip", remote_ip)

                # Best-effort reverse DNS (skip if it would slow things down too much)
                try:
                    hostname = socket.gethostbyaddr(remote_ip)[0]
                    if hostname and "." in hostname:
                        add("domain", hostname.lower())
                except (socket.herror, socket.gaierror, OSError, socket.timeout):
                    pass
    except (psutil.AccessDenied, PermissionError):
        pass
    except Exception:
        pass

    return observations


def collect_process_network_hints(limit: int = 50) -> List[Dict[str, Any]]:
    """Lightweight process + remote IP summary for operator reports."""
    if psutil is None:
        return []

    hints = []
    try:
        for proc in psutil.process_iter(["pid", "name", "username"]):
            if len(hints) >= limit:
                break
            try:
                conns = proc.connections(kind="inet")
                remote_ips = list({str(c.raddr.ip) for c in conns if c.raddr})
                if remote_ips:
                    hints.append({
                        "pid": proc.info["pid"],
                        "name": proc.info["name"],
                        "user": proc.info.get("username"),
                        "remote_ips": remote_ips[:8],
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception:
        pass

    return hints


def privilege_check() -> Dict[str, Any]:
    """Simple check of what visibility is available."""
    result = {"psutil": psutil is not None, "full_connections": False, "note": ""}
    if psutil is None:
        result["note"] = "psutil not installed — limited functionality"
        return result
    try:
        list(psutil.net_connections(kind="inet"))
        result["full_connections"] = True
        result["note"] = "Full connection visibility available"
    except (psutil.AccessDenied, PermissionError):
        result["note"] = "Insufficient privileges for full connection list — run with appropriate rights for best results"
    except Exception as e:
        result["note"] = f"Visibility limited: {e}"
    return result
