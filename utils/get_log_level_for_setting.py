
def get_log_level_for_setting(config: Config, *setting_names: str) -> int | None:
    for setting_name in setting_names:
        log_level = config.getoption(setting_name)
        if log_level is None:
            log_level = config.getini(setting_name)
        if log_level:
            break
    else:
        return None

    if isinstance(log_level, str):
        log_level = log_level.upper()
    try:
        return int(getattr(logging, log_level, log_level))
    except ValueError as e:
        # Python logging does not recognise this as a logging level
        raise UsageError(
            f"'{log_level}' is not recognized as a logging level name for "
            f"'{setting_name}'. Please consider passing the "
            "logging level num instead."
        ) from e

