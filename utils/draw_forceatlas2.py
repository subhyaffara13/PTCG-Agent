
def draw_forceatlas2(G, **kwargs):
    """Draw a networkx graph with forceatlas2 layout.

    This is a convenience function equivalent to::

       nx.draw(G, pos=nx.forceatlas2_layout(G), **kwargs)

    Parameters
    ----------
    G : graph
       A networkx graph

    kwargs : optional keywords
       See networkx.draw_networkx() for a description of optional keywords,
       with the exception of the pos parameter which is not used by this
       function.
    """
    draw(G, pos=nx.forceatlas2_layout(G), **kwargs)

