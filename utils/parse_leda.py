
def parse_leda(lines):
    """Read graph in LEDA format from string or iterable.

    Parameters
    ----------
    lines : string or iterable
       Data in LEDA format.

    Returns
    -------
    G : NetworkX graph

    Examples
    --------
    >>> G = nx.parse_leda(string)  # doctest: +SKIP

    References
    ----------
    .. [1] http://www.algorithmic-solutions.info/leda_guide/graphs/leda_native_graph_fileformat.html
    """
    if isinstance(lines, str):
        lines = iter(lines.split("\n"))
    lines = iter(
        [
            line.rstrip("\n")
            for line in lines
            if not (line.startswith(("#", "\n")) or line == "")
        ]
    )
    for i in range(3):
        next(lines)
    # Graph
    du = int(next(lines))  # -1=directed, -2=undirected
    if du == -1:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    # Nodes
    n = int(next(lines))  # number of nodes
    node = {}
    for i in range(1, n + 1):  # LEDA counts from 1 to n
        symbol = next(lines).rstrip().strip("|{}|  ")
        if symbol == "":
            symbol = str(i)  # use int if no label - could be trouble
        node[i] = symbol

    G.add_nodes_from([s for i, s in node.items()])

    # Edges
    m = int(next(lines))  # number of edges
    for i in range(m):
        try:
            s, t, reversal, label = next(lines).split()
        except BaseException as err:
            raise NetworkXError(f"Too few fields in LEDA.GRAPH edge {i + 1}") from err
        # BEWARE: no handling of reversal edges
        G.add_edge(node[int(s)], node[int(t)], label=label[2:-2])
    return G

