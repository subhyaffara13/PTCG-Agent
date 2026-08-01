
def sorted_components_inner(
    graph: Graph, vertices: AbstractSet[str], pri_max: int
) -> list[AbstractSet[str]]:
    """Simplified version of sorted_components() to work with sub-graphs.

    This doesn't create SCC objects, and operates with raw sets. This function
    also allows filtering dependencies to take into account when building SCCs.
    This is used for heuristic ordering of modules within actual SCCs.
    """
    edges = {id: deps_filtered(graph, vertices, id, pri_max) for id in vertices}
    sccs = list(strongly_connected_components(vertices, edges))
    res = []
    for ready in topsort(prepare_sccs(sccs, edges)):
        res.extend(sorted(ready, key=lambda scc: -min(graph[id].order for id in scc)))
    return res

