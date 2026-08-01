
def is_running_from_reloader() -> bool:
    """Check if the server is running as a subprocess within the
    Werkzeug reloader.

    .. versionadded:: 0.10
    """
    return os.environ.get("WERKZEUG_RUN_MAIN") == "true"

