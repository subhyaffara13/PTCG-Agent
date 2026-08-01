
def check_create_using(create_using, *, directed=None, multigraph=None, default=None):
    """Assert that create_using has good properties

    This checks for desired directedness and multi-edge properties.
    It returns `create_using` unless that is `None` when it returns
    the optionally specified default value.

    Parameters
    ----------
    create_using : None, graph class or instance
        The input value of create_using for a function.
    directed : None or bool
        Whether to check `create_using.is_directed() == directed`.
        If None, do not assert directedness.
    multigraph : None or bool
        Whether to check `create_using.is_multigraph() == multigraph`.
        If None, do not assert multi-edge property.
    default : None or graph class
        The graph class to return if create_using is None.

    Returns
    -------
    create_using : graph class or instance
        The provided graph class or instance, or if None, the `default` value.

    Raises
    ------
    NetworkXError
        When `create_using` doesn't match the properties specified by `directed`
        or `multigraph` parameters.
    """
    if default is None:
        default = nx.Graph
    G = create_using if create_using is not None else default

    G_directed = G.is_directed(None) if isinstance(G, type) else G.is_directed()
    G_multigraph = G.is_multigraph(None) if isinstance(G, type) else G.is_multigraph()

    if directed is not None:
        if directed and not G_directed:
            raise nx.NetworkXError("create_using must be directed")
        if not directed and G_directed:
            raise nx.NetworkXError("create_using must not be directed")

    if multigraph is not None:
        if multigraph and not G_multigraph:
            raise nx.NetworkXError("create_using must be a multi-graph")
        if not multigraph and G_multigraph:
            raise nx.NetworkXError("create_using must not be a multi-graph")
    return G

