
def marimo_version():
    """Marimo's version number"""
    try:
        return marimo("--version").strip()
    except OSError:
        return "N/A"

