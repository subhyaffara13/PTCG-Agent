
def is_semieulerian(G):
    """Return True iff `G` is semi-Eulerian.

    G is semi-Eulerian if it has an Eulerian path but no Eulerian circuit.

    See Also
    --------
    has_eulerian_path
    is_eulerian
    """
    return has_eulerian_path(G) and not is_eulerian(G)

