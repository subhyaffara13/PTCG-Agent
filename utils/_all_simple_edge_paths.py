
def _all_simple_edge_paths(G, source, targets, cutoff):
    # We simulate recursion with a stack, keeping the current path being explored
    # and the outgoing edge iterators at each point in the stack.
    # To avoid unnecessary checks, the loop is structured in a way such that a path
    # is considered for yielding only after a new node/edge is added.
    # We bootstrap the search by adding a dummy iterator to the stack that only yields
    # a dummy edge to source (so that the trivial path has a chance of being included).

    get_edges = (
        (lambda node: G.edges(node, keys=True))
        if G.is_multigraph()
        else (lambda node: G.edges(node))
    )

    # The current_path is a dictionary that maps nodes in the path to the edge that was
    # used to enter that node (instead of a list of edges) because we want both a fast
    # membership test for nodes in the path and the preservation of insertion order.
    current_path = {None: None}
    stack = [iter([(None, source)])]

    while stack:
        # 1. Try to extend the current path.
        next_edge = next((e for e in stack[-1] if e[1] not in current_path), None)
        if next_edge is None:
            # All edges of the last node in the current path have been explored.
            stack.pop()
            current_path.popitem()
            continue
        previous_node, next_node, *_ = next_edge

        # 2. Check if we've reached a target.
        if next_node in targets:
            yield (list(current_path.values()) + [next_edge])[2:]  # remove dummy edge

        # 3. Only expand the search through the next node if it makes sense.
        if len(current_path) - 1 < cutoff and (
            targets - current_path.keys() - {next_node}
        ):
            current_path[next_node] = next_edge
            stack.append(iter(get_edges(next_node)))

