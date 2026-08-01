
def find_unloaded_deps(
    manager: BuildManager, graph: dict[str, State], initial: Sequence[str]
) -> list[str]:
    """Find all the deps of the nodes in initial that haven't had their tree loaded.

    The key invariant here is that if a module is loaded, so are all
    of their dependencies. This means that when we encounter a loaded
    module, we don't need to explore its dependencies.  (This
    invariant is slightly violated when dependencies are added, which
    can be handled by calling find_unloaded_deps directly on the new
    dependencies.)
    """
    worklist = list(initial)
    seen: set[str] = set()
    unloaded = []
    while worklist:
        node = worklist.pop()
        if node in seen or node not in graph:
            continue
        seen.add(node)
        if node not in manager.modules:
            ancestors = graph[node].ancestors or []
            worklist.extend(graph[node].dependencies + ancestors)
            unloaded.append(node)

    return unloaded

