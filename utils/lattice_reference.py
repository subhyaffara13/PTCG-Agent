
def lattice_reference(G, niter=5, D=None, connectivity=True, seed=None):
    """Latticize the given graph by swapping edges.

    Parameters
    ----------
    G : graph
        An undirected graph.

    niter : integer (optional, default=1)
        An edge is rewired approximately niter times.

    D : numpy.array (optional, default=None)
        Distance to the diagonal matrix.

    connectivity : boolean (optional, default=True)
        Ensure connectivity for the latticized graph when set to True.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    G : graph
        The latticized graph.

    Raises
    ------
    NetworkXError
        If there are fewer than 4 nodes or 2 edges in `G`

    Notes
    -----
    The implementation is adapted from the algorithm by Sporns et al. [1]_.
    which is inspired from the original work by Maslov and Sneppen(2002) [2]_.

    References
    ----------
    .. [1] Sporns, Olaf, and Jonathan D. Zwi.
       "The small world of the cerebral cortex."
       Neuroinformatics 2.2 (2004): 145-162.
    .. [2] Maslov, Sergei, and Kim Sneppen.
       "Specificity and stability in topology of protein networks."
       Science 296.5569 (2002): 910-913.
    """
    import numpy as np

    from networkx.utils import cumulative_distribution, discrete_sequence

    local_conn = nx.connectivity.local_edge_connectivity

    if len(G) < 4:
        raise nx.NetworkXError("Graph has fewer than four nodes.")
    if len(G.edges) < 2:
        raise nx.NetworkXError("Graph has fewer that 2 edges")
    # Instead of choosing uniformly at random from a generated edge list,
    # this algorithm chooses nonuniformly from the set of nodes with
    # probability weighted by degree.
    G = G.copy()
    keys, degrees = zip(*G.degree())  # keys, degree
    cdf = cumulative_distribution(degrees)  # cdf of degree

    nnodes = len(G)
    nedges = nx.number_of_edges(G)
    if D is None:
        D = np.zeros((nnodes, nnodes))
        un = np.arange(1, nnodes)
        um = np.arange(nnodes - 1, 0, -1)
        u = np.append((0,), np.where(un < um, un, um))

        for v in range(int(np.ceil(nnodes / 2))):
            D[nnodes - v - 1, :] = np.append(u[v + 1 :], u[: v + 1])
            D[v, :] = D[nnodes - v - 1, :][::-1]

    niter = niter * nedges
    # maximal number of rewiring attempts per 'niter'
    max_attempts = int(nnodes * nedges / (nnodes * (nnodes - 1) / 2))

    for _ in range(niter):
        n = 0
        while n < max_attempts:
            # pick two random edges without creating edge list
            # choose source node indices from discrete distribution
            (ai, ci) = discrete_sequence(2, cdistribution=cdf, seed=seed)
            if ai == ci:
                continue  # same source, skip
            a = keys[ai]  # convert index to label
            c = keys[ci]
            # choose target uniformly from neighbors
            b = seed.choice(list(G.neighbors(a)))
            d = seed.choice(list(G.neighbors(c)))
            bi = keys.index(b)
            di = keys.index(d)

            if b in [a, c, d] or d in [a, b, c]:
                continue  # all vertices should be different

            # don't create parallel edges
            if (d not in G[a]) and (b not in G[c]):
                if D[ai, bi] + D[ci, di] >= D[ai, ci] + D[bi, di]:
                    # only swap if we get closer to the diagonal
                    G.add_edge(a, d)
                    G.add_edge(c, b)
                    G.remove_edge(a, b)
                    G.remove_edge(c, d)

                    # Check if the graph is still connected
                    if connectivity and local_conn(G, a, b) == 0:
                        # Not connected, revert the swap
                        G.remove_edge(a, d)
                        G.remove_edge(c, b)
                        G.add_edge(a, b)
                        G.add_edge(c, d)
                    else:
                        break
            n += 1

    return G

