
def get_known_modules(
    stdlib_versions: StdlibVersions | None = None, python_version: tuple[int, int] | None = None
) -> frozenset[str]:
    global _known_modules_cache
    if _known_modules_cache is not None:
        return _known_modules_cache
    modules: set[str] = set(POPULAR_THIRD_PARTY_MODULES)
    if stdlib_versions is not None:
        modules = modules.union(get_stdlib_modules(stdlib_versions, python_version))
    _known_modules_cache = frozenset(modules)
    return _known_modules_cache

