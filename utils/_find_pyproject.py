
def _find_pyproject() -> Path:
    """Search for file pyproject.toml in the parent directories recursively.

    It resolves symlinks, so if there is any symlink up in the tree, it does not respect them
    """
    current_dir = Path.cwd().resolve()
    is_root = False
    while not is_root:
        if (current_dir / PYPROJECT_NAME).is_file():
            return current_dir / PYPROJECT_NAME
        is_root = (
            current_dir == current_dir.parent
            or (current_dir / ".git").is_dir()
            or (current_dir / ".hg").is_dir()
        )
        current_dir = current_dir.parent

    return current_dir

