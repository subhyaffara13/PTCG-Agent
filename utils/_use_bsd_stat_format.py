import os

def _use_bsd_stat_format():
    try:
        return os.uname().sysname.lower() in ("freebsd", "netbsd", "dragonfly")
    except Exception:
        return False

