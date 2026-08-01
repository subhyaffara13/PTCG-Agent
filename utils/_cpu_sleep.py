
def _cpu_sleep(cycles: int) -> None:
    """Spin-wait for approximately the given number of cycles."""
    for _ in range(cycles):
        pass

