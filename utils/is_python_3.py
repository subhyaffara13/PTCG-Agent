import sys

def is_python_3():
    """Check if the Python interpreter is Python 2 or 3.

    Returns:
        bool: True if the Python interpreter is Python 3 and False otherwise.
    """

    return sys.version_info > (3, 0)  # pragma: NO COVER

