
def get_config_var(name: Literal["SO"]) -> int | str | None: ...


def get_config_var(name: str) -> int | str | None: ...


def get_config_var(name: str) -> int | str | None:
    """Return the value of a single variable using the dictionary
    returned by 'get_config_vars()'.  Equivalent to
    get_config_vars().get(name)
    """
    if name == 'SO':
        import warnings

        warnings.warn('SO is deprecated, use EXT_SUFFIX', DeprecationWarning, 2)
    return get_config_vars().get(name)

