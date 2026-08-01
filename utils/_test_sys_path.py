
def _test_sys_path(
    replacement_sys_path: list[str] | None = None,
) -> Generator[None]:
    original_path = sys.path
    try:
        if replacement_sys_path is not None:
            sys.path = copy(replacement_sys_path)
        yield
    finally:
        sys.path = original_path

