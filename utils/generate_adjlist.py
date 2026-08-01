
def generate_adjlist(G, delimiter=" "):
    """Generate lines representing a graph in adjacency list format.

    Parameters
    ----------
    G : NetworkX graph

    delimiter : str, default=" "
        Separator for node labels.

    Yields
    ------
    str
        Adjacency list for a node in `G`. The first item is the node label,
        followed by the labels of its neighbors.

    Examples
    --------
    >>> G = nx.lollipop_graph(4, 3)
    >>> for line in nx.generate_adjlist(G):
    ...     print(line)
    0 1 2 3
    1 2 3
    2 3
    3 4
    4 5
    5 6
    6

    When `G` is undirected, each edge is only listed once. For directed graphs,
    edges appear once for each direction.

    >>> G = nx.complete_graph(3, create_using=nx.DiGraph)
    >>> for line in nx.generate_adjlist(G):
    ...     print(line)
    0 1 2
    1 0 2
    2 0 1

    Node labels are shown multiple times for multiedges, but edge data (including keys)
    are not included in the output.

    >>> G = nx.MultiGraph([(0, 1, {"weight": 1}), (0, 1, {"weight": 2})])
    >>> for line in nx.generate_adjlist(G):
    ...     print(line)
    0 1 1
    1

    See Also
    --------
    write_adjlist, read_adjlist

    Notes
    -----
    The default `delimiter=" "` will result in unexpected results if node names contain
    whitespace characters. To avoid this problem, specify an alternate delimiter when spaces are
    valid in node names.

    NB: This option is not available for data that isn't user-generated.

    """
    seen = set()
    directed = G.is_directed()
    multigraph = G.is_multigraph()
    for s, nbrs in G.adjacency():
        nodes = [str(s)]
        for t, data in nbrs.items():
            if t in seen:
                continue
            if multigraph and len(data) > 1:
                nodes.extend((str(t),) * len(data))
            else:
                nodes.append(str(t))
        if not directed:
            seen.add(s)
        yield delimiter.join(nodes)

