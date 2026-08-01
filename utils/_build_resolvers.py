
def _build_resolvers(paths: Iterable[str]) -> dict[str, Any]:
    resolvers = {}
    for path in paths:
        if path in resolvers:
            continue

        pyproject = _load_pyproject(path)
        if "dependency-groups" not in pyproject:
            raise InstallationError(
                f"[dependency-groups] table was missing from '{path}'. "
                "Cannot resolve '--group' option."
            )
        raw_dependency_groups = pyproject["dependency-groups"]
        if not isinstance(raw_dependency_groups, dict):
            raise InstallationError(
                f"[dependency-groups] table was malformed in {path}. "
                "Cannot resolve '--group' option."
            )

        try:
            resolvers[path] = DependencyGroupResolver(raw_dependency_groups)
        except ExceptionGroup as eg:
            # Handle ExceptionGroup from resolver initialization
            messages = [str(e) for e in eg.exceptions]
            raise InstallationError(
                f"[dependency-groups] data was invalid in {path}: {'; '.join(messages)}"
            ) from eg

    return resolvers

