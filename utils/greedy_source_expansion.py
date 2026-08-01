
def greedy_source_expansion(G, *, source, cutoff=None, method="clauset"):
    r"""Find the local community around a source node.

    Find the local community around a source node using Greedy Source
    Expansion. Greedy Source Expansion generally identifies a local community
    starting from the source node and expands it based on the criteria of the
    chosen algorithm.

    The algorithm is specified with the `method` keyword argument.

    * `"clauset"` [1]_ uses local modularity gain to determine local communities.
        The algorithm adds nbring nodes that maximize local modularity to the
        community iteratively, stopping when no additional nodes improve the modularity
        or when a predefined cutoff is reached.

        Local modularity measures the density of edges within a community relative
        to the total graph. By focusing on local modularity, the algorithm efficiently
        uncovers communities around a specific node without requiring global
        optimization over the entire graph.

        The algorithm assumes that the graph $G$ consists of a known community $C$ and
        an unknown set of nodes $U$, which are adjacent to $C$ . The boundary of the
        community $B$, consists of nodes in $C$ that have at least one nbr in $U$.

        Mathematically, the local modularity is expressed as:

        .. math::
            R = \frac{I}{T}

        where $T$ is the number of edges with one or more endpoints in $B$, and $I$ is the
        number of those edges with neither endpoint in $U$.

    Parameters
    ----------
    G : NetworkX graph
        The input graph.

    source : node
        The source node from which the community expansion begins.

    cutoff : int, optional (default=None)
        The maximum number of nodes to include in the community. If None, the algorithm
        expands until no further modularity gain can be made.

    method : string, optional (default='clauset')
        The algorithm to use to carry out greedy source expansion.
        Supported options: 'clauset'. Other inputs produce a ValueError

    Returns
    -------
    set
        A set of nodes representing the local community around the source node.

    Examples
    --------
    >>> G = nx.karate_club_graph()
    >>> nx.community.greedy_source_expansion(G, source=16)
    {16, 0, 4, 5, 6, 10}

    Notes
    -----
    This algorithm is designed for detecting local communities around a specific node,
    which is useful for large networks where global community detection is computationally
    expensive.

    The result of the algorithm may vary based on the structure of the graph, the choice of
    the source node, and the presence of ties between nodes during the greedy expansion process.

    References
    ----------
    .. [1] Clauset, Aaron. Finding local community structure in networks.
      Physical Review E—Statistical, Nonlinear, and Soft Matter Physics 72, no. 2 (2005): 026132.
      https://arxiv.org/pdf/physics/0503036

    """
    try:
        algo = ALGORITHMS[method]
    except KeyError as e:
        raise ValueError(f"{method} is not a valid choice for an algorithm.") from e

    return algo(G, source=source, cutoff=cutoff)

