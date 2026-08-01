
def multigraph_cycle_edgeset(c):
    if len(c) <= 2:
        return frozenset(cycle_edges(c))
    else:
        return frozenset(map(frozenset, cycle_edges(c)))

