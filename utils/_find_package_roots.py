
def _find_package_roots(
    packages: Iterable[str],
    package_dir: Mapping[str, str],
    src_root: StrPath,
) -> dict[str, str]:
    pkg_roots: dict[str, str] = {
        pkg: _absolute_root(find_package_path(pkg, package_dir, src_root))
        for pkg in sorted(packages)
    }

    return _remove_nested(pkg_roots)

