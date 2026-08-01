
def disable_logging(log):
    disabled = log.disabled
    log.disabled = True
    try:
        yield
    finally:
        log.disabled = disabled

