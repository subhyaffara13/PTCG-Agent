
def tournament_matrix(G):
    r"""Returns the tournament matrix for the given tournament graph.

    This function requires SciPy.

    The *tournament matrix* of a tournament graph with edge set *E* is
    the matrix *T* defined by

    .. math::

       T_{i j} =
       \begin{cases}
       +1 & \text{if } (i, j) \in E \\
       -1 & \text{if } (j, i) \in E \\
       0 & \text{if } i == j.
       \end{cases}

    An equivalent definition is `T = A - A^T`, where *A* is the
    adjacency matrix of the graph `G`.

    Parameters
    ----------
    G : NetworkX graph
        A directed graph representing a tournament.

    Returns
    -------
    SciPy sparse array
        The tournament matrix of the tournament graph `G`.

    Raises
    ------
    ImportError
        If SciPy is not available.

    """
    A = nx.adjacency_matrix(G)
    return A - A.T

