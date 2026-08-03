from pathlib import Path


def _dep_source_from_project_path(
    project_path: Path, index_url: str, extra_index_urls: list[str], locked: bool, state: AuditState
) -> DependencySource:  # pragma: no cover
    # If the user has passed `--locked`, we check for `pylock.*.toml` files.
    if locked:
        all_pylocks = list(project_path.glob("pylock.*.toml"))
        generic_pylock = project_path / "pylock.toml"
        if generic_pylock.is_file():
            all_pylocks.append(generic_pylock)

        if not all_pylocks:
            _fatal(f"no lockfiles found in {project_path}")

        return PyLockSource(all_pylocks)

    # Check for a `pyproject.toml`
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.is_file():
        return PyProjectSource(
            pyproject_path,
            index_url=index_url,
            extra_index_urls=extra_index_urls,
            state=state,
        )

    # TODO: Checks for setup.py and other project files will go here.

    _fatal(f"couldn't find a supported project file in {project_path}")

