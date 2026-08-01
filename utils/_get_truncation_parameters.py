
def _get_truncation_parameters(item: Item) -> tuple[bool, int, int]:
    """Return the truncation parameters related to the given item, as (should truncate, max lines, max chars)."""
    # We do not need to truncate if one of conditions is met:
    # 1. Verbosity level is 2 or more;
    # 2. Test is being run in CI environment;
    # 3. Both truncation_limit_lines and truncation_limit_chars
    #    .ini parameters are set to 0 explicitly.
    max_lines = item.config.getini("truncation_limit_lines")
    max_lines = int(max_lines if max_lines is not None else DEFAULT_MAX_LINES)

    max_chars = item.config.getini("truncation_limit_chars")
    max_chars = int(max_chars if max_chars is not None else DEFAULT_MAX_CHARS)

    verbose = item.config.get_verbosity(Config.VERBOSITY_ASSERTIONS)

    should_truncate = verbose < 2 and not running_on_ci()
    should_truncate = should_truncate and (max_lines > 0 or max_chars > 0)

    return should_truncate, max_lines, max_chars

