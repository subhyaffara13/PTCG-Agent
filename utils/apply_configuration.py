
def apply_configuration(
    dist: Distribution,
    filepath: StrPath,
    ignore_option_errors: bool = False,
) -> Distribution:
    """Apply the configuration from a ``pyproject.toml`` file into an existing
    distribution object.
    """
    config = read_configuration(filepath, True, ignore_option_errors, dist)
    return _apply(dist, config, filepath)


def apply_configuration(dist: Distribution, filepath: StrPath) -> Distribution:
    """Apply the configuration from a ``setup.cfg`` file into an existing
    distribution object.
    """
    _apply(dist, filepath)
    dist._finalize_requires()
    return dist

