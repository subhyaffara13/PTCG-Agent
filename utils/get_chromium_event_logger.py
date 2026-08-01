
def get_chromium_event_logger() -> ChromiumEventLogger:
    global CHROMIUM_EVENT_LOG
    if CHROMIUM_EVENT_LOG is None:
        CHROMIUM_EVENT_LOG = ChromiumEventLogger()
    return CHROMIUM_EVENT_LOG

