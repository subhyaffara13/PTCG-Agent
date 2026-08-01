
def _get_deps_info():
    """
    Get the versions of the dependencies.

    Returns
    -------
    dict
        Versions of the dependencies.
    """
    deps = ["cobyqa", "numpy", "scipy", "setuptools", "pip"]
    deps_info = {}
    for module in deps:
        try:
            deps_info[module] = version(module)
        except PackageNotFoundError:
            deps_info[module] = None
    return deps_info

