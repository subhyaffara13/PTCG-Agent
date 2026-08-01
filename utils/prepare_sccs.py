
def prepare_sccs(
    sccs: list[set[T]], edges: dict[T, list[T]]
) -> dict[AbstractSet[T], set[AbstractSet[T]]]:
    """Use original edges to organize SCCs in a graph by dependencies between them."""
    sccsmap = {}
    for scc in sccs:
        scc_frozen = frozenset(scc)
        for v in scc:
            sccsmap[v] = scc_frozen
    data: dict[AbstractSet[T], set[AbstractSet[T]]] = {}
    for scc in sccs:
        deps: set[AbstractSet[T]] = set()
        for v in scc:
            deps.update(sccsmap[x] for x in edges[v])
        data[frozenset(scc)] = deps
    return data

