
def turan_graph(n, r):
    r"""Return the Turan Graph

    The Turan Graph is a complete multipartite graph on $n$ nodes
    with $r$ disjoint subsets. That is, edges connect each node to
    every node not in its subset.

    Given $n$ and $r$, we create a complete multipartite graph with
    $r-(n \mod r)$ partitions of size $n/r$, rounded down, and
    $n \mod r$ partitions of size $n/r+1$, rounded down.

    .. plot::

        >>> nx.draw(nx.turan_graph(6, 2))

    Parameters
    ----------
    n : int
        The number of nodes.
    r : int
        The number of partitions.
        Must be less than or equal to n.

    Notes
    -----
    Must satisfy $1 <= r <= n$.
    The graph has $(r-1)(n^2)/(2r)$ edges, rounded down.
    """

    if not 1 <= r <= n:
        raise NetworkXError("Must satisfy 1 <= r <= n")

    partitions = [n // r] * (r - (n % r)) + [n // r + 1] * (n % r)
    G = complete_multipartite_graph(*partitions)
    return G

