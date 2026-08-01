
def _find_packages_within(root_pkg: str, pkg_dir: StrPath) -> list[str]:
    nested = PEP420PackageFinder.find(pkg_dir)
    return [root_pkg] + [".".join((root_pkg, n)) for n in nested]

