
def parse_p2g(lines):
    """Parse p2g format graph from string or iterable.

    Returns
    -------
    MultiDiGraph
    """
    description = next(lines).strip()
    # are multiedges (parallel edges) allowed?
    G = nx.MultiDiGraph(name=description, selfloops=True)
    nnodes, nedges = map(int, next(lines).split())
    nodelabel = {}
    nbrs = {}
    # loop over the nodes keeping track of node labels and out neighbors
    # defer adding edges until all node labels are known
    for i in range(nnodes):
        n = next(lines).strip()
        nodelabel[i] = n
        G.add_node(n)
        nbrs[n] = map(int, next(lines).split())
    # now we know all of the node labels so we can add the edges
    # with the correct labels
    for n in G:
        for nbr in nbrs[n]:
            G.add_edge(n, nodelabel[nbr])
    return G

