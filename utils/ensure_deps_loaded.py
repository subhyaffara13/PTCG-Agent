
def ensure_deps_loaded(module: str, deps: dict[str, set[str]], graph: dict[str, State]) -> None:
    """Ensure that the dependencies on a module are loaded.

    Dependencies are loaded into the 'deps' dictionary.

    This also requires loading dependencies from any parent modules,
    since dependencies will get stored with parent modules when a module
    doesn't exist.
    """
    if module in graph and graph[module].fine_grained_deps_loaded:
        return
    parts = module.split(".")
    for i in range(len(parts)):
        base = ".".join(parts[: i + 1])
        if base in graph and not graph[base].fine_grained_deps_loaded:
            merge_dependencies(graph[base].load_fine_grained_deps(), deps)
            graph[base].fine_grained_deps_loaded = True

