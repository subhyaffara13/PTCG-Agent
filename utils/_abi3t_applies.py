
def _abi3t_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3t.

    PEP 803 was first implemented in Python 3.15 but, per PEP 803, this
    returns tags going back to Python 3.2 to mirror the abi3
    implementation and leave open the possibility of abi3t wheels
    supporting older Python versions.

    """
    return len(python_version) > 1 and tuple(python_version) >= (3, 2) and threading


def _abi3t_applies(python_version: PythonVersion, threading: bool) -> bool:
    """
    Determine if the Python version supports abi3t.

    PEP 803 was first implemented in Python 3.15 but, per PEP 803, this
    returns tags going back to Python 3.2 to mirror the abi3
    implementation and leave open the possibility of abi3t wheels
    supporting older Python versions.

    """
    return len(python_version) > 1 and tuple(python_version) >= (3, 2) and threading

