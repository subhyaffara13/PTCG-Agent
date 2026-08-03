import os

def _test_environ_pythonpath(
    new_pythonpath: str | None = None,
) -> Generator[None]:
    original_pythonpath = os.environ.get("PYTHONPATH")
    if new_pythonpath:
        os.environ["PYTHONPATH"] = new_pythonpath
    elif new_pythonpath is None and original_pythonpath is not None:
        # If new_pythonpath is None, make sure to delete PYTHONPATH if present
        del os.environ["PYTHONPATH"]
    try:
        yield
    finally:
        if original_pythonpath is not None:
            os.environ["PYTHONPATH"] = original_pythonpath
        elif "PYTHONPATH" in os.environ:
            del os.environ["PYTHONPATH"]

