
def _create_model_pyproject(repo_dir: Path):
    """
    Creates a `pyproject.toml` for the repository.

    Args:
        repo_dir (`Path`):
            Directory where `pyproject.toml` is created.
    """
    pyproject_path = repo_dir / "pyproject.toml"

    if not pyproject_path.exists():
        with pyproject_path.open("w", encoding="utf-8") as f:
            f.write(PYPROJECT_TEMPLATE)

