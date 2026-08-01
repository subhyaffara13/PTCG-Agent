
def expand_configuration(
    config: dict,
    root_dir: StrPath | None = None,
    ignore_option_errors: bool = False,
    dist: Distribution | None = None,
) -> dict:
    """Given a configuration with unresolved fields (e.g. dynamic, cmdclass, ...)
    find their final values.

    :param dict config: Dict containing the configuration for the distribution
    :param str root_dir: Top-level directory for the distribution/project
        (the same directory where ``pyproject.toml`` is place)
    :param bool ignore_option_errors: see :func:`read_configuration`
    :param Distribution|None: Distribution object to which the configuration refers.
        If not given a dummy object will be created and discarded after the
        configuration is read. Used in the case a dynamic configuration
        (e.g. ``attr`` or ``cmdclass``).

    :rtype: dict
    """
    return _ConfigExpander(config, root_dir, ignore_option_errors, dist).expand()

