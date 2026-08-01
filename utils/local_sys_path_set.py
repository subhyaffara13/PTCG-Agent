
def local_sys_path_set() -> Iterator[None]:
    """Temporary insert current directory into sys.path.

    This can be used by test cases that do runtime imports, for example
    by the stubgen tests.
    """
    old_sys_path = sys.path.copy()
    if not ("" in sys.path or "." in sys.path):
        sys.path.insert(0, "")
    try:
        yield
    finally:
        sys.path = old_sys_path

