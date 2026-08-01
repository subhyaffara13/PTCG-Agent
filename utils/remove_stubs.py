
def remove_stubs(packages: list[str]) -> list[str]:
    """Remove type stubs (:pep:`561`) from a list of packages.

    >>> remove_stubs(["a", "a.b", "a-stubs", "a-stubs.b.c", "b", "c-stubs"])
    ['a', 'a.b', 'b']
    """
    return [pkg for pkg in packages if not pkg.split(".")[0].endswith("-stubs")]

