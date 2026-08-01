
def filter_out_missing_top_level_packages(
    packages: set[str], search_paths: SearchPaths, fscache: FileSystemCache
) -> set[str]:
    """Quickly filter out obviously missing top-level packages.

    Return packages with entries that can't be found removed.

    This is approximate: some packages that aren't actually valid may be
    included. However, all potentially valid packages must be returned.
    """
    # Start with a empty set and add all potential top-level packages.
    found = set()
    paths = (
        search_paths.python_path
        + search_paths.mypy_path
        + search_paths.package_path
        + search_paths.typeshed_path
    )
    for p in paths:
        try:
            entries = fscache.listdir(p)
        except Exception:
            entries = []
        for entry in entries:
            # The code is hand-optimized for mypyc since this may be somewhat
            # performance-critical.
            if entry.endswith(".py"):
                entry = entry[:-3]
            elif entry.endswith(".pyi"):
                entry = entry[:-4]
            elif entry.endswith("-stubs"):
                # Possible PEP 561 stub package
                entry = entry[:-6]
            if entry in packages:
                found.add(entry)
    return found

