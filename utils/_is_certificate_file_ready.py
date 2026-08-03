import os

def _is_certificate_file_ready(path):
    """Checks if a file exists and is not empty."""
    return path and os.path.exists(path) and os.path.getsize(path) > 0

