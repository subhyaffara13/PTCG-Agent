
def parse_dependency_groups(groups: list[tuple[str, str]]) -> list[str]:
    """
    Parse dependency groups data as provided via the CLI, in a `[path:]group` syntax.

    Raises InstallationErrors if anything goes wrong.
    """
    resolvers = _build_resolvers(path for (path, _) in groups)
    return list(_resolve_all_groups(resolvers, groups))

