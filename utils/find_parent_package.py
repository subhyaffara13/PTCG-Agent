import os

def find_parent_package(
    packages: list[str], package_dir: Mapping[str, str], root_dir: StrPath
) -> str | None:
    """Find the parent package that is not a namespace."""
    packages = sorted(packages, key=len)
    common_ancestors = []
    for i, name in enumerate(packages):
        if not all(n.startswith(f"{name}.") for n in packages[i + 1 :]):
            # Since packages are sorted by length, this condition is able
            # to find a list of all common ancestors.
            # When there is divergence (e.g. multiple root packages)
            # the list will be empty
            break
        common_ancestors.append(name)

    for name in common_ancestors:
        pkg_path = find_package_path(name, package_dir, root_dir)
        init = os.path.join(pkg_path, "__init__.py")
        if os.path.isfile(init):
            return name

    return None

