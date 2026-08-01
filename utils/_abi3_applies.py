
def _abi3_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2. The free-threaded
    builds do not support abi3.
    """
    return len(python_version) > 1 and tuple(python_version) >= (3, 2) and not threading


def _abi3_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2. The threaded (`--disable-gil`)
    builds do not support abi3.
    """
    return len(python_version) > 1 and tuple(python_version) >= (3, 2) and not threading


def _abi3_applies(python_version: PythonVersion) -> bool:
    """
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2.
    """
    return len(python_version) > 1 and tuple(python_version) >= (3, 2)


def _abi3_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3.

    PEP 384 was first implemented in Python 3.2. The free-threaded
    builds do not support abi3.
    """
    return len(python_version) > 1 and tuple(python_version) >= (3, 2) and not threading

