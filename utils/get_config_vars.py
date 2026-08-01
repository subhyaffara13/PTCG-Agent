
def get_config_vars() -> dict[str, str | int]: ...


def get_config_vars(arg: str, /, *args: str) -> list[str | int]: ...


def get_config_vars(*args: str) -> list[str | int] | dict[str, str | int]:
    """With no arguments, return a dictionary of all configuration
    variables relevant for the current platform.  Generally this includes
    everything needed to build extensions and install both pure modules and
    extensions.  On Unix, this means every variable defined in Python's
    installed Makefile; on Windows it's a much smaller set.

    With arguments, return a list of values that result from looking up
    each argument in the configuration variable dictionary.
    """
    global _config_vars
    if _config_vars is None:
        _config_vars = sysconfig.get_config_vars().copy()
        py39.add_ext_suffix(_config_vars)

    return [_config_vars.get(name) for name in args] if args else _config_vars

