
def _make_module_path_relative(abs_path: str, sys_path: tuple[str, ...]) -> str:
    """
    The string manipulation here is fairly expensive and we expect very high
    cache hit rates. Because `sys.path` changes very infrequently it's most
    performant to convert it into a tuple of strings and use that for the cache
    key because python has dedicated fast paths for list to tuple conversion
    and tuple hashing. (Empirically, a single top-level cache is about 2x faster
    than trying to cache individual parts.)
    """

    abs_path_resolved = pathlib.Path(abs_path).resolve()

    for path in sys_path:
        try:
            rel_path = abs_path_resolved.relative_to(path)
        except ValueError:
            continue
        else:
            return str(rel_path)

    return str(abs_path_resolved)

