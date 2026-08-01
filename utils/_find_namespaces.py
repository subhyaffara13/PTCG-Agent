
def _find_namespaces(
    packages: list[str], pkg_roots: dict[str, str]
) -> Iterator[tuple[str, list[str]]]:
    for pkg in packages:
        path = find_package_path(pkg, pkg_roots, "")
        if Path(path).exists() and not Path(path, "__init__.py").exists():
            yield (pkg, [path])

