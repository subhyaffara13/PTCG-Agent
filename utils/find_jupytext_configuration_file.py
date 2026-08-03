from pathlib import Path


def find_jupytext_configuration_file(path: typing.Union[str, Path], search_parent_dirs=True) -> str:
    """Return the first jupytext configuration file in the current directory, or any parent directory"""

    path = Path(path).absolute()

    if path.is_dir():
        for filename in JUPYTEXT_CONFIG_FILES:
            full_path = path / filename
            if full_path.is_file():
                return str(full_path)

    pyproject_path = path / PYPROJECT_FILE
    if pyproject_path.is_file():
        with pyproject_path.open() as stream:
            doc = tomllib.loads(stream.read())
            if doc.get("tool", {}).get("jupytext") is not None:
                return str(pyproject_path)

    if not search_parent_dirs:
        return None

    if JUPYTEXT_CEILING_DIRECTORIES and path.is_dir():
        for ceiling_dir in JUPYTEXT_CEILING_DIRECTORIES:
            if Path(ceiling_dir).is_dir() and path.absolute() == Path(ceiling_dir).absolute():
                return None

    parent_dir = path.parent
    if parent_dir == path:
        return find_global_jupytext_configuration_file()

    return find_jupytext_configuration_file(parent_dir, True)

