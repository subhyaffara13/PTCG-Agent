
def find_default_config_files() -> Iterator[Path]:
    """Find all possible config files."""
    yield from _yield_default_files()

    try:
        yield from _find_project_config()
    except OSError:
        pass

    try:
        parent_pyproject = _find_pyproject()
        if parent_pyproject.is_file() and _toml_has_config(parent_pyproject):
            yield parent_pyproject.resolve()
    except OSError:
        pass

    try:
        yield from _find_config_in_home_or_environment()
    except OSError:
        pass

    try:
        if os.path.isfile("/etc/pylintrc"):
            yield Path("/etc/pylintrc").resolve()
    except OSError:
        pass

