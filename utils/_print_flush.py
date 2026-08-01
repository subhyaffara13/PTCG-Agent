
def _print_flush(*values: Any, **kwargs: Any) -> None:
    """Like `print`, but always flushed: some CLI flows block on user action right after
    printing (e.g. the device-code login), so output must not stay buffered."""
    print(*values, **kwargs, flush=True)

