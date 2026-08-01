
def is_minimal_d_separator(G, x, y, z, *, included=None, restricted=None):
    """Determine if `z` is a minimal d-separator for `x` and `y`.

    A d-separator, `z`, in a DAG is a set of nodes that blocks
    all paths from nodes in set `x` to nodes in set `y`.
    A minimal d-separator is a d-separator `z` such that removing
    any subset of nodes makes it no longer a d-separator.

    Note: This function checks whether `z` is a d-separator AND is
    minimal. One can use the function `is_d_separator` to only check if
    `z` is a d-separator. See examples below.

    Parameters
    ----------
    G : nx.DiGraph
        A NetworkX DAG.
    x : node | set
        A node or set of nodes in the graph.
    y : node | set
        A node or set of nodes in the graph.
    z : node | set
        The node or set of nodes to check if it is a minimal d-separating set.
        The function :func:`is_d_separator` is called inside this function
        to verify that `z` is in fact a d-separator.
    included : set | node | None
        A node or set of nodes which must be included in the found separating set,
        default is ``None``, which means the empty set.
    restricted : set | node | None
        Restricted node or set of nodes to consider. Only these nodes can be in
        the found separating set, default is ``None`` meaning all nodes in ``G``.

    Returns
    -------
    bool
        Whether or not the set `z` is a minimal d-separator subject to
        `restricted` nodes and `included` node constraints.

    Examples
    --------
    >>> G = nx.path_graph([0, 1, 2, 3], create_using=nx.DiGraph)
    >>> G.add_node(4)
    >>> nx.is_minimal_d_separator(G, 0, 2, {1})
    True
    >>> # since {1} is the minimal d-separator, {1, 3, 4} is not minimal
    >>> nx.is_minimal_d_separator(G, 0, 2, {1, 3, 4})
    False
    >>> # alternatively, if we only want to check that {1, 3, 4} is a d-separator
    >>> nx.is_d_separator(G, 0, 2, {1, 3, 4})
    True

    Raises
    ------
    NetworkXError
        Raises a :exc:`NetworkXError` if the input graph is not a DAG.

    NodeNotFound
        If any of the input nodes are not found in the graph,
        a :exc:`NodeNotFound` exception is raised.

    References
    ----------
    .. [1] van der Zander, Benito, and Maciej Liśkiewicz. "Finding
        minimal d-separators in linear time and applications." In
        Uncertainty in Artificial Intelligence, pp. 637-647. PMLR, 2020.

    Notes
    -----
    This function works on verifying that a set is minimal and
    d-separating between two nodes. Uses criterion (a), (b), (c) on
    page 4 of [1]_. a) closure(`x`) and `y` are disjoint. b) `z` contains
    all nodes from `included` and is contained in the `restricted`
    nodes and in the union of ancestors of `x`, `y`, and `included`.
    c) the nodes in `z` not in `included` are contained in both
    closure(x) and closure(y). The closure of a set is the set of nodes
    connected to the set by a directed path in G.

    The complexity is :math:`O(m)`, where :math:`m` stands for the
    number of edges in the subgraph of G consisting of only the
    ancestors of `x` and `y`.

    For full details, see [1]_.
    """
    if not nx.is_directed_acyclic_graph(G):
        raise nx.NetworkXError("graph should be directed acyclic")

    try:
        x = {x} if x in G else x
        y = {y} if y in G else y
        z = {z} if z in G else z

        if included is None:
            included = set()
        elif included in G:
            included = {included}

        if restricted is None:
            restricted = set(G)
        elif restricted in G:
            restricted = {restricted}

        set_y = x | y | included | restricted
        if set_y - G.nodes:
            raise nx.NodeNotFound(f"The node(s) {set_y - G.nodes} are not found in G")
    except TypeError:
        raise nx.NodeNotFound(
            "One of x, y, z, included or restricted is not a node or set of nodes in G"
        )

    if not included <= z:
        raise nx.NetworkXError(
            f"Included nodes {included} must be in proposed separating set z {x}"
        )
    if not z <= restricted:
        raise nx.NetworkXError(
            f"Separating set {z} must be contained in restricted set {restricted}"
        )

    intersection = x.intersection(y) or x.intersection(z) or y.intersection(z)
    if intersection:
        raise nx.NetworkXError(
            f"The sets are not disjoint, with intersection {intersection}"
        )

    nodeset = x | y | included
    ancestors_x_y_included = nodeset.union(*[nx.ancestors(G, n) for n in nodeset])

    # criterion (a) -- check that z is actually a separator
    x_closure = _reachable(G, x, ancestors_x_y_included, z)
    if x_closure & y:
        return False

    # criterion (b) -- basic constraint; included and restricted already checked above
    if not (z <= ancestors_x_y_included):
        return False

    # criterion (c) -- check that z is minimal
    y_closure = _reachable(G, y, ancestors_x_y_included, z)
    if not ((z - included) <= (x_closure & y_closure)):
        return False
    return True

