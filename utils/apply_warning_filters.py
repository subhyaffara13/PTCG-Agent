
def apply_warning_filters(
    config_filters: Iterable[str], cmdline_filters: Iterable[str]
) -> None:
    """Applies pytest-configured filters to the warnings module"""
    # Filters should have this precedence: cmdline options, config.
    # Filters should be applied in the inverse order of precedence.
    for arg in config_filters:
        try:
            warnings.filterwarnings(*parse_warning_filter(arg, escape=False))
        except ImportError as e:
            warnings.warn(
                f"Failed to import filter module '{e.name}': {arg}", PytestConfigWarning
            )
            continue

    for arg in cmdline_filters:
        try:
            warnings.filterwarnings(*parse_warning_filter(arg, escape=True))
        except ImportError as e:
            warnings.warn(
                f"Failed to import filter module '{e.name}': {arg}", PytestConfigWarning
            )
            continue

