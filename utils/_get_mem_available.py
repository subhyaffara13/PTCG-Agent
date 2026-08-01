
def _get_mem_available():
    """Return available memory in bytes, or None if unknown."""
    try:
        import psutil

        return psutil.virtual_memory().available
    except (ImportError, AttributeError):
        pass

    if sys.platform.startswith("linux"):
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                p = line.split()
                info[p[0].strip(":").lower()] = int(p[1]) * 1024

        if "memavailable" in info:
            # Linux >= 3.14
            return info["memavailable"]
        else:
            return info["memfree"] + info["cached"]

    return None


def _get_mem_available():
    """
    Get information about memory available, not counting swap.
    """
    try:
        import psutil
        return psutil.virtual_memory().available
    except (ImportError, AttributeError):
        pass

    if sys.platform.startswith('linux'):
        info = {}
        with open('/proc/meminfo') as f:
            for line in f:
                p = line.split()
                info[p[0].strip(':').lower()] = float(p[1]) * 1e3

        if 'memavailable' in info:
            # Linux >= 3.14
            return info['memavailable']
        else:
            return info['memfree'] + info['cached']

    return None


def _get_mem_available():
    """Return available memory in bytes, or None if unknown."""
    try:
        import psutil
        return psutil.virtual_memory().available
    except (ImportError, AttributeError):
        pass

    if sys.platform.startswith('linux'):
        info = {}
        with open('/proc/meminfo') as f:
            for line in f:
                p = line.split()
                info[p[0].strip(':').lower()] = int(p[1]) * 1024

        if 'memavailable' in info:
            # Linux >= 3.14
            return info['memavailable']
        else:
            return info['memfree'] + info['cached']

    return None

