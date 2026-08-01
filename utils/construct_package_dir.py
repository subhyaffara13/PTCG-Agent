
def construct_package_dir(packages: list[str], package_path: StrPath) -> dict[str, str]:
    parent_pkgs = remove_nested_packages(packages)
    prefix = Path(package_path).parts
    return {pkg: "/".join([*prefix, *pkg.split(".")]) for pkg in parent_pkgs}

