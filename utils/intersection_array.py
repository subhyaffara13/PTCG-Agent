
def intersection_array(G):
    """Returns the intersection array of a distance-regular graph.

    Given a distance-regular graph G with integers b_i, c_i,i = 0,....,d
    such that for any 2 vertices x,y in G at a distance i=d(x,y), there
    are exactly c_i neighbors of y at a distance of i-1 from x and b_i
    neighbors of y at a distance of i+1 from x.

    A distance regular graph's intersection array is given by,
    [b_0,b_1,.....b_{d-1};c_1,c_2,.....c_d]

    Parameters
    ----------
    G: Networkx graph (undirected)

    Returns
    -------
    b,c: tuple of lists

    Examples
    --------
    >>> G = nx.icosahedral_graph()
    >>> nx.intersection_array(G)
    ([5, 2, 1], [1, 2, 5])

    References
    ----------
    .. [1] Weisstein, Eric W. "Intersection Array."
       From MathWorld--A Wolfram Web Resource.
       http://mathworld.wolfram.com/IntersectionArray.html

    See Also
    --------
    global_parameters
    """
    # the input graph is very unlikely to be distance-regular: here are the
    # number a(n) of connected simple graphs, and the number b(n) of
    # distance-regular graphs among them:
    #
    #    n  | 1 2 3 4  5   6   7     8      9       10
    #  -----+------------------------------------------------------------------
    #  a(n) | 1 1 2 6 21 112 853 11117 261080 11716571 https://oeis.org/A001349
    #  b(n) | 1 1 1 2  2   4   2     5      4        7 https://oeis.org/A241814
    #
    # in light of this, let's compute shortest path lengths as we go instead of
    # precomputing them all
    # test for regular graph (all degrees must be equal)
    if not nx.is_regular(G) or not nx.is_connected(G):
        raise nx.NetworkXError("Graph is not distance regular.")

    path_length = defaultdict(dict)
    bint = {}  # 'b' intersection array
    cint = {}  # 'c' intersection array

    # see https://doi.org/10.1016/j.ejc.2004.07.004, Theorem 1.5, page 81:
    # the diameter of a distance-regular graph is at most (8 log_2 n) / 3,
    # so let's compute it as we go in the hope that we can stop early
    diam = 0
    max_diameter_for_dr_graphs = (8 * log(len(G), 2)) / 3
    for u, v in combinations_with_replacement(G, 2):
        # compute needed shortest path lengths
        pl_u = path_length[u]
        if v not in pl_u:
            pl_u.update(nx.single_source_shortest_path_length(G, u))
            for x, distance in pl_u.items():
                path_length[x][u] = distance

        i = path_length[u][v]
        diam = max(diam, i)

        # diameter too large: graph can't be distance-regular
        if diam > max_diameter_for_dr_graphs:
            raise nx.NetworkXError("Graph is not distance regular.")

        vnbrs = G[v]
        # compute needed path lengths
        for n in vnbrs:
            pl_n = path_length[n]
            if u not in pl_n:
                pl_n.update(nx.single_source_shortest_path_length(G, n))
                for x, distance in pl_n.items():
                    path_length[x][n] = distance

        # number of neighbors of v at a distance of i-1 from u
        c = sum(1 for n in vnbrs if pl_u[n] == i - 1)
        # number of neighbors of v at a distance of i+1 from u
        b = sum(1 for n in vnbrs if pl_u[n] == i + 1)
        # b, c are independent of u and v
        if cint.get(i, c) != c or bint.get(i, b) != b:
            raise nx.NetworkXError("Graph is not distance regular")
        bint[i] = b
        cint[i] = c

    return (
        [bint.get(j, 0) for j in range(diam)],
        [cint.get(j + 1, 0) for j in range(diam)],
    )

