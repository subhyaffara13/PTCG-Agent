
def module_with_reason(name: str, config: Config = DEFAULT_CONFIG) -> tuple[str, str]:
    """Returns the section placement for the given module name alongside the reasoning."""
    return (
        _forced_separate(name, config)
        or _local(name, config)
        or _known_pattern(name, config)
        or _src_path(name, config)
        or (config.default_section, "Default option in Config or universal default.")
    )

