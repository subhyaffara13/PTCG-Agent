
def get_reraise_exceptions(config: Config) -> tuple[type[BaseException], ...]:
    """Return exception types that should not be suppressed in general."""
    reraise: tuple[type[BaseException], ...] = (Exit,)
    if not config.getoption("usepdb", False):
        reraise += (KeyboardInterrupt,)
    return reraise

