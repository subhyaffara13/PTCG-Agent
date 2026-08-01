
def deps_filtered(graph: Graph, vertices: AbstractSet[str], id: str, pri_max: int) -> list[str]:
    """Filter dependencies for id with pri < pri_max."""
    if id not in vertices:
        return []
    state = graph[id]
    return [
        dep
        for dep in state.dependencies
        if dep in vertices and state.priorities.get(dep, PRI_HIGH) < pri_max
    ]

