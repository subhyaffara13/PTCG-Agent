import math


def harmonic_diameter(G, sp=None, *, weight=None):
    """Returns the harmonic diameter of the graph G.

    The harmonic diameter of a graph is the harmonic mean of the distances
    between all pairs of distinct vertices. Graphs that are not strongly
    connected have infinite diameter and mean distance, making such
    measures not useful. Restricting the diameter or mean distance to
    finite distances yields paradoxical values (e.g., a perfect match
    would have diameter one). The harmonic mean handles gracefully
    infinite distances (e.g., a perfect match has harmonic diameter equal
    to the number of vertices minus one), making it possible to assign a
    meaningful value to all graphs.

    Note that in [1] the harmonic diameter is called "connectivity length":
    however, "harmonic diameter" is a more standard name from the
    theory of metric spaces. The name "harmonic mean distance" is perhaps
    a more descriptive name, but is not used in the literature, so we use the
    name "harmonic diameter" here.

    Parameters
    ----------
    G : NetworkX graph
       A graph

    sp : dict of dicts, optional
       All-pairs shortest path lengths as a dictionary of dictionaries

    weight : string, function, or None (default=None)
        If None, every edge has weight/distance 1.
        If a string, use this edge attribute as the edge weight.
        Any edge attribute not present defaults to 1.
        If a function, the weight of an edge is the value returned by the function.
        The function must accept exactly three positional arguments:
        the two endpoints of an edge and the dictionary of edge attributes for
        that edge. The function must return a number.

    Returns
    -------
    hd : float
       Harmonic diameter of graph

    References
    ----------
    .. [1] Massimo Marchiori and Vito Latora, "Harmony in the small-world".
           *Physica A: Statistical Mechanics and Its Applications*
           285(3-4), pages 539-546, 2000.
           <https://doi.org/10.1016/S0378-4371(00)00311-3>
    """
    order = G.order()

    sum_invd = 0
    for n in G:
        if sp is None:
            length = nx.single_source_dijkstra_path_length(G, n, weight=weight)
        else:
            try:
                length = sp[n]
                L = len(length)
            except TypeError as err:
                raise nx.NetworkXError('Format of "sp" is invalid.') from err

        for d in length.values():
            # Note that this will skip the zero distance from n to itself,
            # as it should be, but also zero-weight paths in weighted graphs.
            if d != 0:
                sum_invd += 1 / d

    if sum_invd != 0:
        return order * (order - 1) / sum_invd
    if order > 1:
        return math.inf
    return math.nan

