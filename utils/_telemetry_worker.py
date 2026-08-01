
def _telemetry_worker():
    """Wait for a task and consume it."""
    while True:
        kwargs = _TELEMETRY_QUEUE.get()
        _send_telemetry_in_thread(**kwargs)
        _TELEMETRY_QUEUE.task_done()

