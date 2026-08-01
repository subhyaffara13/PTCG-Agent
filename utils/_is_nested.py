
def _is_nested(pkg: str, pkg_path: str, parent: str, parent_path: str) -> bool:
    """
    Return ``True`` if ``pkg`` is nested inside ``parent`` both logically and in the
    file system.
    >>> _is_nested("a.b", "path/a/b", "a", "path/a")
    True
    >>> _is_nested("a.b", "path/a/b", "a", "otherpath/a")
    False
    >>> _is_nested("a.b", "path/a/b", "c", "path/c")
    False
    >>> _is_nested("a.a", "path/a/a", "a", "path/a")
    True
    >>> _is_nested("b.a", "path/b/a", "a", "path/a")
    False
    """
    norm_pkg_path = _path.normpath(pkg_path)
    rest = pkg.replace(parent, "", 1).strip(".").split(".")
    return pkg.startswith(parent) and norm_pkg_path == _path.normpath(
        Path(parent_path, *rest)
    )

