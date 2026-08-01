
def _get_module_and_submodules(qname: str) -> Sequence[str] | None:
    """
    Get a module and all its submodules (recursively).

    If qname is a package, this returns a list of all modules and submodules.
    If qname is a simple module, this returns a list containing just that module.

    Args:
        qname: The fully qualified module name

    Returns:
        A list of fully qualified module names, or None if the module doesn't exist
    """
    spec = importlib.util.find_spec(qname)
    if spec is None:
        return None

    modules = [qname]

    if spec.submodule_search_locations is not None:
        package = importlib.import_module(qname)
        if hasattr(package, "__path__"):
            for importer, modname, ispkg in pkgutil.walk_packages(
                path=package.__path__,
                prefix=qname + ".",
                onerror=lambda x: None,
            ):
                modules.append(modname)

    return modules

