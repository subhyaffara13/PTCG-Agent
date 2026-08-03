import sys
from typing import Any

def get_meminfo() -> dict[str, Any]:
    res: dict[str, Any] = {}
    try:
        import psutil
    except ImportError:
        res["memory_psutil_missing"] = (
            "psutil not found, run pip install mypy[dmypy] "
            "to install the needed components for dmypy"
        )
    else:
        process = psutil.Process()
        meminfo = process.memory_info()
        res["memory_rss_mib"] = meminfo.rss / MiB
        res["memory_vms_mib"] = meminfo.vms / MiB
        if sys.platform == "win32":
            res["memory_maxrss_mib"] = meminfo.peak_wset / MiB
        else:
            # See https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
            import resource  # Since it doesn't exist on Windows.

            rusage = resource.getrusage(resource.RUSAGE_SELF)
            if sys.platform == "darwin":
                factor = 1
            else:
                factor = 1024  # Linux
            res["memory_maxrss_mib"] = rusage.ru_maxrss * factor / MiB
    return res

