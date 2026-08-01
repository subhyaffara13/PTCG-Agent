
def _should_use_dd_profiler():
    """Returns True if `USE_DDPROFILER` is set to True in .env"""
    return get_secret_bool("USE_DDPROFILER", False) is True

