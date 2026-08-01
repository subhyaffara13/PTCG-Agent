
def draw_bipartite(G, **kwargs):
    """Draw the graph `G` with a bipartite layout.

    This is a convenience function equivalent to::

        nx.draw(G, pos=nx.bipartite_layout(G), **kwargs)

    Parameters
    ----------
    G : graph
        A networkx graph

    kwargs : optional keywords
        See `draw_networkx` for a description of optional keywords.

    Raises
    ------
    NetworkXError :
        If `G` is not bipartite.

    Notes
    -----
    The layout is computed each time this function is called. For
    repeated drawing it is much more efficient to call
    `~networkx.drawing.layout.bipartite_layout` directly and reuse the result::

        >>> G = nx.complete_bipartite_graph(3, 3)
        >>> pos = nx.bipartite_layout(G)
        >>> nx.draw(G, pos=pos)  # Draw the original graph
        >>> # Draw a subgraph, reusing the same node positions
        >>> nx.draw(G.subgraph([0, 1, 2]), pos=pos, node_color="red")

    Examples
    --------
    >>> G = nx.complete_bipartite_graph(2, 5)
    >>> nx.draw_bipartite(G)

    See Also
    --------
    :func:`~networkx.drawing.layout.bipartite_layout`
    """
    draw(G, pos=nx.bipartite_layout(G), **kwargs)

