
def get_flag(
    var: str, fallback: bool, expected: bool = True, warn: bool = True
) -> bool:
    """Use a fallback value for determining SOABI flags if the needed config
    var is unset or unavailable."""
    val = sysconfig.get_config_var(var)
    if val is None:
        if warn:
            warnings.warn(
                f"Config variable '{var}' is unset, Python ABI tag may be incorrect",
                RuntimeWarning,
                stacklevel=2,
            )
        return fallback
    return val == expected


def get_flag(
    var: str, fallback: bool, expected: bool = True, warn: bool = True
) -> bool:
    """Use a fallback value for determining SOABI flags if the needed config
    var is unset or unavailable."""
    val = sysconfig.get_config_var(var)
    if val is None:
        if warn:
            warnings.warn(
                f"Config variable '{var}' is unset, Python ABI tag may be incorrect",
                RuntimeWarning,
                stacklevel=2,
            )
        return fallback
    return val == expected

