import re

def strip_python_stderr(stderr):
    """Strip debug-build refcount output from stderr."""
    return re.sub(b"\\[\\d+ refs\\]\\r?\\n?$", b"", stderr).strip()

