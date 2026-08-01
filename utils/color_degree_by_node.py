
def color_degree_by_node(G, n_colors, e_colors):
    """Returns a dict by node to counts of edge and node color for that node.

    This returns a dict by node to a 2-tuple of node color and degree by
    (edge color and nbr color). E.g. ``{0: (1, {(0, 2): 5})}`` means that
    node ``0`` has node type 1 and has 5 edges of type 0 that go to nodes of type 2.
    Thus, this is a measure of degree (edge count) by color of edge and color
    of the node on the other side of that edge.

    For directed graphs the degree counts is a 2-tuple of (in, out) degree counts.

    Ideally, if edge_match is None, this could get simplified to just the node
    color on the other end of the edge. Similarly if node_match is None then only
    edge color is tracked. And if both are None, we simply count the number of edges.
    """
    # n_colors might be incomplete when using `largest_common_subgraph()`
    if len(n_colors) < len(G):
        for n, nbrs in G.adjacency():
            if n not in n_colors:
                n_colors[n] = None
                for v in nbrs:
                    e_colors[n, v] = None
    # undirected colored degree
    if not G.is_directed():
        return {
            u: (n_colors[u], Counter((e_colors[u, v], n_colors[v]) for v in nbrs))
            for u, nbrs in G.adjacency()
        }
    # directed colored out and in degree
    return {
        u: (
            n_colors[u],
            Counter((e_colors[u, v], n_colors[v]) for v in nbrs),
            Counter((e_colors[v, u], n_colors[v]) for v in G._pred[u]),
        )
        for u, nbrs in G.adjacency()
    }

