
def _has_input(fd: int, timeout: float) -> bool:
    r, _, _ = select.select([fd], [], [], timeout)
    return bool(r)

