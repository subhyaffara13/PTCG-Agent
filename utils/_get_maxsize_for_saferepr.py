
def _get_maxsize_for_saferepr(config: Config | None) -> int | None:
    """Get `maxsize` configuration for saferepr based on the given config object."""
    if config is None:
        verbosity = 0
    else:
        verbosity = config.get_verbosity(Config.VERBOSITY_ASSERTIONS)
    if verbosity >= 2:
        return None
    if verbosity >= 1:
        return DEFAULT_REPR_MAX_SIZE * 10
    return DEFAULT_REPR_MAX_SIZE

