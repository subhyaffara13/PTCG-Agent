
def connected_cuthill_mckee_ordering(G, heuristic=None):
    # the cuthill mckee algorithm for connected graphs
    if heuristic is None:
        start = pseudo_peripheral_node(G)
    else:
        start = heuristic(G)
    visited = {start}
    queue = deque([start])
    while queue:
        parent = queue.popleft()
        yield parent
        nd = sorted(G.degree(set(G[parent]) - visited), key=itemgetter(1))
        children = [n for n, d in nd]
        visited.update(children)
        queue.extend(children)

