
def stop_debug_server() -> None:
    """
    Shutdown the debug server and stop the frontend debug server process.
    """
    global _WORKER_SERVER, _DEBUG_SERVER_PROC

    if _DEBUG_SERVER_PROC is None:
        raise AssertionError
    if _WORKER_SERVER is None:
        raise AssertionError

    logger.info("Stopping debug server")

    _DEBUG_SERVER_PROC.terminate()
    _WORKER_SERVER.shutdown()
    _DEBUG_SERVER_PROC.join()

    _WORKER_SERVER = None
    _DEBUG_SERVER_PROC = None

