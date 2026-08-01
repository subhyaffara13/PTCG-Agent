
def _should_use_dd_tracer():
    """Returns True if `USE_DDTRACE` is set to True in .env"""
    return get_secret_bool("USE_DDTRACE", False) is True

