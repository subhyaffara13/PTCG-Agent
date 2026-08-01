
def exist_removed_submodules(dependencies: list[str], manager: BuildManager) -> bool:
    """Find if there are any submodules of packages that are now missing.

    This is conceptually an inverse of exist_added_packages().
    """
    dependencies_set = set(dependencies)
    for dep in dependencies:
        if "." not in dep:
            continue
        if dep in manager.source_set.source_modules:
            # We still know it is definitely a module.
            continue
        direct_ancestor, _ = dep.rsplit(".", maxsplit=1)
        if direct_ancestor not in dependencies_set:
            continue
        if find_module_simple(dep, manager) is None:
            return True
    return False

