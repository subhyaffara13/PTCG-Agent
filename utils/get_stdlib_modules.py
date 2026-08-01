
def get_stdlib_modules(
    stdlib_versions: StdlibVersions, python_version: tuple[int, int] | None = None
) -> frozenset[str]:
    modules: set[str] = set()
    for module, (min_ver, max_ver) in stdlib_versions.items():
        if python_version is not None:
            if python_version < min_ver:
                continue
            if max_ver is not None and python_version > max_ver:
                continue
        top_level = module.split(".")[0]
        # Skip private and very short modules to avoid false positives and noise
        if top_level.startswith("_") or len(top_level) <= 2:
            continue
        modules.add(top_level)
    return frozenset(modules)

