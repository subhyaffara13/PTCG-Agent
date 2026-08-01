
def _cpu_get_cpuinfo_freq():
    """Return current CPU frequency from cpuinfo if available."""
    with open_binary(f"{get_procfs_path()}/cpuinfo") as f:
        return [
            float(line.split(b':', 1)[1])
            for line in f
            if line.lower().startswith(b'cpu mhz')
        ]

