
def fix_module_deps(graph: mypy.build.Graph) -> None:
    """After an incremental update, update module dependencies to reflect the new state.

    This can make some suppressed dependencies non-suppressed, and vice versa (if modules
    have been added to or removed from the build).
    """
    for state in graph.values():
        new_suppressed = []
        new_dependencies = []
        for dep in state.dependencies + state.suppressed:
            if dep in graph:
                new_dependencies.append(dep)
            else:
                new_suppressed.append(dep)
        state.dependencies = new_dependencies
        state.dependencies_set = set(new_dependencies)
        state.suppressed = new_suppressed
        state.suppressed_set = set(new_suppressed)

