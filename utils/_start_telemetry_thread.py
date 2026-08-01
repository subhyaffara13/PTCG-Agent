
def _start_telemetry_thread():
    """Start a daemon thread to consume tasks from the telemetry queue.

    If the thread is interrupted, start a new one.
    """
    with _TELEMETRY_THREAD_LOCK:  # avoid to start multiple threads if called concurrently
        global _TELEMETRY_THREAD
        if _TELEMETRY_THREAD is None or not _TELEMETRY_THREAD.is_alive():
            _TELEMETRY_THREAD = Thread(target=_telemetry_worker, daemon=True)
            _TELEMETRY_THREAD.start()

