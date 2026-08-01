
def cpu_freq():
    """Return CPU frequency.
    On Windows per-cpu frequency is not supported.
    """
    curr, max_ = cext.cpu_freq()
    min_ = 0.0
    return [ntp.scpufreq(float(curr), min_, float(max_))]

