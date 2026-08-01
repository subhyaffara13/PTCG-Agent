
def is_running(status_file: str) -> bool:
    """Check if the server is running cleanly"""
    try:
        get_status(status_file)
    except BadStatus:
        return False
    return True

