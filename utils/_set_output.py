
def _set_output(run: Run, value: str | None) -> None:
    """Set the output."""
    assert value is not None
    run._output = value

