
def find_relative_leaf_module(modules: list[tuple[str, str]], graph: Graph) -> tuple[str, str]:
    """Find a module in a list that directly imports no other module in the list.

    If no such module exists, return the lexicographically first module from the list.
    Always return one of the items in the modules list.

    NOTE: If both 'abc' and 'typing' have changed, an effect of the above rule is that
        we prefer 'abc', even if both are in the same SCC. This works around a false
        positive in 'typing', at least in tests.

    Args:
        modules: List of (module, path) tuples (non-empty)
        graph: Program import graph that contains all modules in the module list
    """
    assert modules
    # Sort for repeatable results.
    modules = sorted(modules)
    module_set = {module for module, _ in modules}
    for module, path in modules:
        state = graph[module]
        if len(set(state.dependencies) & module_set) == 0:
            # Found it!
            return module, path
    # Could not find any. Just return the first module (by lexicographic order).
    return modules[0]

