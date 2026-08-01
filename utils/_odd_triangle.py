
def _odd_triangle(G, T):
    """Test whether T is an odd triangle in G

    Parameters
    ----------
    G : NetworkX Graph
    T : 3-tuple of vertices forming triangle in G

    Returns
    -------
    True is T is an odd triangle
    False otherwise

    Raises
    ------
    NetworkXError
        T is not a triangle in G

    Notes
    -----
    An odd triangle is one in which there exists another vertex in G which is
    adjacent to either exactly one or exactly all three of the vertices in the
    triangle.

    """
    for u in T:
        if u not in G.nodes():
            raise nx.NetworkXError(f"Vertex {u} not in graph")
    for e in list(combinations(T, 2)):
        if e[0] not in G[e[1]]:
            raise nx.NetworkXError(f"Edge ({e[0]}, {e[1]}) not in graph")

    T_nbrs = defaultdict(int)
    for t in T:
        for v in G[t]:
            if v not in T:
                T_nbrs[v] += 1
    return any(T_nbrs[v] in [1, 3] for v in T_nbrs)

