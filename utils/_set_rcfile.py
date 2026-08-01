
def _set_rcfile(run: Run, value: str | None) -> None:
    """Set the rcfile."""
    assert value is not None
    run._rcfile = value

