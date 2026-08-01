
def parse_toml(config_file: str) -> dict[str, Any] | None:
    """Returns a dict of config keys to values.

    It reads configs from toml file and returns `None` if the file is not a toml file.
    """
    if not config_file.endswith('.toml'):
        return None

    if sys.version_info >= (3, 11):
        import tomllib as toml_
    else:
        try:
            import tomli as toml_
        except ImportError:  # pragma: no cover
            import warnings

            warnings.warn('No TOML parser installed, cannot read configuration from `pyproject.toml`.', stacklevel=2)
            return None

    with open(config_file, 'rb') as rf:
        return toml_.load(rf)


def parse_toml(config_file: str) -> Optional[Dict[str, Any]]:
    if not config_file.endswith('.toml'):
        return None

    read_mode = 'rb'
    if sys.version_info >= (3, 11):
        import tomllib as toml_
    else:
        try:
            import tomli as toml_
        except ImportError:
            # older versions of mypy have toml as a dependency, not tomli
            read_mode = 'r'
            try:
                import toml as toml_  # type: ignore[no-redef]
            except ImportError:  # pragma: no cover
                import warnings

                warnings.warn('No TOML parser installed, cannot read configuration from `pyproject.toml`.')
                return None

    with open(config_file, read_mode) as rf:
        return toml_.load(rf)  # type: ignore[arg-type]

