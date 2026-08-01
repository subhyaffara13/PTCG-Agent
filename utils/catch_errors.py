
def catch_errors(module_path: str, line: int) -> Iterator[None]:
    try:
        yield
    except Exception:
        crash_report(module_path, line)

