
def eppstein_matching(G, top_nodes=None):
    """Returns the maximum cardinality matching of the bipartite graph `G`.

    Parameters
    ----------
    G : NetworkX graph

      Undirected bipartite graph

    top_nodes : container

      Container with all nodes in one bipartite node set. If not supplied
      it will be computed. But if more than one solution exists an exception
      will be raised.

    Returns
    -------
    matches : dictionary

      The matching is returned as a dictionary, `matching`, such that
      ``matching[v] == w`` if node `v` is matched to node `w`. Unmatched
      nodes do not occur as a key in `matching`.

    Raises
    ------
    AmbiguousSolution
      Raised if the input bipartite graph is disconnected and no container
      with all nodes in one bipartite set is provided. When determining
      the nodes in each bipartite set more than one valid solution is
      possible if the input graph is disconnected.

    Notes
    -----
    This function is implemented with David Eppstein's version of the algorithm
    Hopcroft--Karp algorithm (see :func:`hopcroft_karp_matching`), which
    originally appeared in the `Python Algorithms and Data Structures library
    (PADS) <http://www.ics.uci.edu/~eppstein/PADS/ABOUT-PADS.txt>`_.

    See :mod:`bipartite documentation <networkx.algorithms.bipartite>`
    for further details on how bipartite graphs are handled in NetworkX.

    See Also
    --------

    hopcroft_karp_matching

    """
    # Due to its original implementation, a directed graph is needed
    # so that the two sets of bipartite nodes can be distinguished
    left, right = bipartite_sets(G, top_nodes)
    G = nx.DiGraph(G.edges(left))
    # initialize greedy matching (redundant, but faster than full search)
    matching = {}
    for u in G:
        for v in G[u]:
            if v not in matching:
                matching[v] = u
                break
    while True:
        # structure residual graph into layers
        # pred[u] gives the neighbor in the previous layer for u in U
        # preds[v] gives a list of neighbors in the previous layer for v in V
        # unmatched gives a list of unmatched vertices in final layer of V,
        # and is also used as a flag value for pred[u] when u is in the first
        # layer
        preds = {}
        unmatched = []
        pred = {u: unmatched for u in G}
        for v in matching:
            del pred[matching[v]]
        layer = list(pred)

        # repeatedly extend layering structure by another pair of layers
        while layer and not unmatched:
            newLayer = {}
            for u in layer:
                for v in G[u]:
                    if v not in preds:
                        newLayer.setdefault(v, []).append(u)
            layer = []
            for v in newLayer:
                preds[v] = newLayer[v]
                if v in matching:
                    layer.append(matching[v])
                    pred[matching[v]] = v
                else:
                    unmatched.append(v)

        # did we finish layering without finding any alternating paths?
        if not unmatched:
            # TODO - The lines between --- were unused and were thus commented
            # out. This whole commented chunk should be reviewed to determine
            # whether it should be built upon or completely removed.
            # ---
            # unlayered = {}
            # for u in G:
            #     # TODO Why is extra inner loop necessary?
            #     for v in G[u]:
            #         if v not in preds:
            #             unlayered[v] = None
            # ---
            # TODO Originally, this function returned a three-tuple:
            #
            #     return (matching, list(pred), list(unlayered))
            #
            # For some reason, the documentation for this function
            # indicated that the second and third elements of the returned
            # three-tuple would be the vertices in the left and right vertex
            # sets, respectively, that are also in the maximum independent set.
            # However, what I think the author meant was that the second
            # element is the list of vertices that were unmatched and the third
            # element was the list of vertices that were matched. Since that
            # seems to be the case, they don't really need to be returned,
            # since that information can be inferred from the matching
            # dictionary.

            # All the matched nodes must be a key in the dictionary
            for key in matching.copy():
                matching[matching[key]] = key
            return matching

        # recursively search backward through layers to find alternating paths
        # recursion returns true if found path, false otherwise
        def recurse(v):
            if v in preds:
                L = preds.pop(v)
                for u in L:
                    if u in pred:
                        pu = pred.pop(u)
                        if pu is unmatched or recurse(pu):
                            matching[v] = u
                            return True
            return False

        for v in unmatched:
            recurse(v)

