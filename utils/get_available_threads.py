
def get_available_threads() -> int:
    """Determine number of physical cores that current process can use (best effort)."""
    global _AVAILABLE_THREADS
    if _AVAILABLE_THREADS is not None:
        return _AVAILABLE_THREADS

    # This takes into account -X cpu_count and/or PYTHON_CPU_COUNT, but always
    # counts virtual cores (which is not what we want for CPU bound tasks).
    os_cpu_count = os.cpu_count()
    if PSUTIL_AVAILABLE:
        # Unlike os, psutil can determine number of physical cores.
        psutil_cpu_count = psutil.cpu_count(logical=False)
    else:
        psutil_cpu_count = None

    if psutil_cpu_count and os_cpu_count:
        cpu_count = min(psutil_cpu_count, os_cpu_count)
    elif psutil_cpu_count or os_cpu_count:
        cpu_count = psutil_cpu_count or os_cpu_count
    else:
        # A conservative fallback in case we cannot determine CPU count in any way.
        cpu_count = 4

    affinity: set[int] | list[int] | None = None
    # Not available on old Python versions on some platforms.
    if sys.platform == "linux":
        affinity = os.sched_getaffinity(0)
    if PSUTIL_AVAILABLE and sys.platform != "darwin":
        # Currently not supported on macOS.
        affinity = psutil.Process().cpu_affinity()

    assert cpu_count is not None
    if affinity:
        available_threads = min(cpu_count, len(affinity))
    else:
        available_threads = cpu_count
    _AVAILABLE_THREADS = available_threads
    return available_threads

