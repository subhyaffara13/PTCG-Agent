
def undirected_cycle_edgeset(c):
    if len(c) == 1:
        return frozenset(cycle_edges(c))
    return frozenset(map(frozenset, cycle_edges(c)))

