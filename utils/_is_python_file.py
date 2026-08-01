
def _is_python_file(filename: str) -> bool:
    """Return true if the given filename should be considered as a python file.

    .pyc and .pyo are ignored
    """
    return filename.endswith((".py", ".pyi", ".so", ".pyd", ".pyw"))


def _is_python_file(filename):
    '''Check if a file is a Python source file.'''
    if (
        filename == '-'
        or filename.endswith('.py')
        or (SUPPORTS_IPYNB and filename.endswith('.ipynb'))
    ):
        return True
    try:
        with open(filename) as fobj:
            first_line = fobj.readline()
            if first_line.startswith('#!') and 'python' in first_line:
                return True
    except Exception:
        return False
    return False

