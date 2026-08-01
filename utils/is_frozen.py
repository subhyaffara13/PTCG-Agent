
def is_frozen(G):
    """Returns True if graph is frozen.

    Parameters
    ----------
    G : graph
      A NetworkX graph

    See Also
    --------
    freeze
    """
    try:
        return G.frozen
    except AttributeError:
        return False

