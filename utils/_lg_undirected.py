
def _lg_undirected(G, selfloops=False, create_using=None):
    """Returns the line graph L of the (multi)graph G.

    Edges in G appear as nodes in L, represented as sorted tuples of the form
    (u,v), or (u,v,key) if G is a multigraph. A node in L corresponding to
    the edge {u,v} is connected to every node corresponding to an edge that
    involves u or v.

    Parameters
    ----------
    G : graph
        An undirected graph or multigraph.
    selfloops : bool
        If `True`, then self-loops are included in the line graph. If `False`,
        they are excluded.
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
       Graph type to create. If graph instance, then cleared before populated.

    Notes
    -----
    The standard algorithm for line graphs of undirected graphs does not
    produce self-loops.

    """
    L = nx.empty_graph(0, create_using, default=G.__class__)

    # Graph specific functions for edges.
    get_edges = partial(G.edges, keys=True) if G.is_multigraph() else G.edges

    # Determine if we include self-loops or not.
    shift = 0 if selfloops else 1

    # Introduce numbering of nodes
    node_index = {n: i for i, n in enumerate(G)}

    # Lift canonical representation of nodes to edges in line graph
    def edge_key_function(edge):
        return node_index[edge[0]], node_index[edge[1]]

    edges = set()
    for u in G:
        # Label nodes as a sorted tuple of nodes in original graph.
        # Decide on representation of {u, v} as (u, v) or (v, u) depending on node_index.
        # -> This ensures a canonical representation and avoids comparing values of different types.
        nodes = [tuple(sorted(x[:2], key=node_index.get)) + x[2:] for x in get_edges(u)]

        if len(nodes) == 1:
            # Then the edge will be an isolated node in L.
            L.add_node(nodes[0])

        # Add a clique of `nodes` to graph. To prevent double adding edges,
        # especially important for multigraphs, we store the edges in
        # canonical form in a set.
        for i, a in enumerate(nodes):
            edges.update(
                [
                    tuple(sorted((a, b), key=edge_key_function))
                    for b in nodes[i + shift :]
                ]
            )

    L.add_edges_from(edges)
    return L

