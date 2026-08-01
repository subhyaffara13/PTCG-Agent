
def _is_connected_by_alternating_path(G, v, matched_edges, unmatched_edges, targets):
    """Returns True if and only if the vertex `v` is connected to one of
    the target vertices by an alternating path in `G`.

    An *alternating path* is a path in which every other edge is in the
    specified maximum matching (and the remaining edges in the path are not in
    the matching). An alternating path may have matched edges in the even
    positions or in the odd positions, as long as the edges alternate between
    'matched' and 'unmatched'.

    `G` is an undirected bipartite NetworkX graph.

    `v` is a vertex in `G`.

    `matched_edges` is a set of edges present in a maximum matching in `G`.

    `unmatched_edges` is a set of edges not present in a maximum
    matching in `G`.

    `targets` is a set of vertices.

    """

    def _alternating_dfs(u, along_matched=True):
        """Returns True if and only if `u` is connected to one of the
        targets by an alternating path.

        `u` is a vertex in the graph `G`.

        If `along_matched` is True, this step of the depth-first search
        will continue only through edges in the given matching. Otherwise, it
        will continue only through edges *not* in the given matching.

        """
        visited = set()
        # Follow matched edges when depth is even,
        # and follow unmatched edges when depth is odd.
        initial_depth = 0 if along_matched else 1
        stack = [(u, iter(G[u]), initial_depth)]
        while stack:
            parent, children, depth = stack[-1]
            valid_edges = matched_edges if depth % 2 else unmatched_edges
            try:
                child = next(children)
                if child not in visited:
                    if (parent, child) in valid_edges or (child, parent) in valid_edges:
                        if child in targets:
                            return True
                        visited.add(child)
                        stack.append((child, iter(G[child]), depth + 1))
            except StopIteration:
                stack.pop()
        return False

    # Check for alternating paths starting with edges in the matching, then
    # check for alternating paths starting with edges not in the
    # matching.
    return _alternating_dfs(v, along_matched=True) or _alternating_dfs(
        v, along_matched=False
    )

