
def _add_plugins(run: Run, value: str | None) -> None:
    """Add plugins to the list of loadable plugins."""
    assert value is not None
    run._plugins.extend(utils._splitstrip(value))

