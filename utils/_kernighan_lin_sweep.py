
def _kernighan_lin_sweep(edge_info, side):
    """
    This is a modified form of Kernighan-Lin, which moves single nodes at a
    time, alternating between sides to keep the bisection balanced.  We keep
    two min-heaps of swap costs to make optimal-next-move selection fast.
    """
    heap0, heap1 = cost_heaps = nx.utils.BinaryHeap(), nx.utils.BinaryHeap()
    # we use heap methods insert, pop, and get
    for u, nbrs in edge_info.items():
        cost_u = sum(wt if side[v] else -wt for v, wt in nbrs.items())
        if side[u]:
            heap1.insert(u, cost_u)
        else:
            heap0.insert(u, -cost_u)

    def _update_heap_values(node):
        side_node = side[node]
        for nbr, wt in edge_info[node].items():
            side_nbr = side[nbr]
            if side_nbr == side_node:
                wt = -wt
            heap_nbr = cost_heaps[side_nbr]
            if nbr in heap_nbr:
                cost_nbr = heap_nbr.get(nbr) + 2 * wt
                # allow_increase lets us update a value already on the heap
                heap_nbr.insert(nbr, cost_nbr, allow_increase=True)

    i = 0
    totcost = 0
    while heap0 and heap1:
        u, cost_u = heap0.pop()
        _update_heap_values(u)
        v, cost_v = heap1.pop()
        _update_heap_values(v)
        totcost += cost_u + cost_v
        i += 1
        yield totcost, i, (u, v)

