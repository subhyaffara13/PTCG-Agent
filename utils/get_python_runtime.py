
def get_python_runtime() -> str:
    try:
        return platform.python_implementation()
    except Exception:
        return "unknown"

