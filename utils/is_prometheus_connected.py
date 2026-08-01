
def is_prometheus_connected() -> bool:
    if PROMETHEUS_URL is not None:
        return True
    return False

