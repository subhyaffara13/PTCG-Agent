
def _configuration_model(
    deg_sequence, create_using, directed=False, in_deg_sequence=None, seed=None
):
    """Helper function for generating either undirected or directed
    configuration model graphs.

    ``deg_sequence`` is a list of nonnegative integers representing the
    degree of the node whose label is the index of the list element.

    ``create_using`` see :func:`~networkx.empty_graph`.

    ``directed`` and ``in_deg_sequence`` are required if you want the
    returned graph to be generated using the directed configuration
    model algorithm. If ``directed`` is ``False``, then ``deg_sequence``
    is interpreted as the degree sequence of an undirected graph and
    ``in_deg_sequence`` is ignored. Otherwise, if ``directed`` is
    ``True``, then ``deg_sequence`` is interpreted as the out-degree
    sequence and ``in_deg_sequence`` as the in-degree sequence of a
    directed graph.

    .. note::

       ``deg_sequence`` and ``in_deg_sequence`` need not be the same
       length.

    ``seed`` is a random.Random or numpy.random.RandomState instance

    This function returns a graph, directed if and only if ``directed``
    is ``True``, generated according to the configuration model
    algorithm. For more information on the algorithm, see the
    :func:`configuration_model` or :func:`directed_configuration_model`
    functions.

    """
    n = len(deg_sequence)
    G = nx.empty_graph(n, create_using)
    # If empty, return the null graph immediately.
    if n == 0:
        return G
    # Build a list of available degree-repeated nodes.  For example,
    # for degree sequence [3, 2, 1, 1, 1], the "stub list" is
    # initially [0, 0, 0, 1, 1, 2, 3, 4], that is, node 0 has degree
    # 3 and thus is repeated 3 times, etc.
    #
    # Also, shuffle the stub list in order to get a random sequence of
    # node pairs.
    if directed:
        pairs = zip_longest(deg_sequence, in_deg_sequence, fillvalue=0)
        # Unzip the list of pairs into a pair of lists.
        out_deg, in_deg = zip(*pairs)

        out_stublist = _to_stublist(out_deg)
        in_stublist = _to_stublist(in_deg)

        seed.shuffle(out_stublist)
        seed.shuffle(in_stublist)
    else:
        stublist = _to_stublist(deg_sequence)
        # Choose a random balanced bipartition of the stublist, which
        # gives a random pairing of nodes. In this implementation, we
        # shuffle the list and then split it in half.
        n = len(stublist)
        half = n // 2
        seed.shuffle(stublist)
        out_stublist, in_stublist = stublist[:half], stublist[half:]
    G.add_edges_from(zip(out_stublist, in_stublist))
    return G

