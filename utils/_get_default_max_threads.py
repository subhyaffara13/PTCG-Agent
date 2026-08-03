import os

def _get_default_max_threads() -> int:
    if DEFAULT_MAX_THREADS:
        return DEFAULT_MAX_THREADS
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    else:
        return os.cpu_count() or 1

