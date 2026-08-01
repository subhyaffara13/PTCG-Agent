
def spectral_modularity_bipartition(G):
    r"""Return a bipartition of the nodes based on the spectrum of the
    modularity matrix of the graph.

    This method calculates the eigenvector associated with the second
    largest eigenvalue of the modularity matrix, where the modularity
    matrix *B* is defined by

    ..math::

        B_{i j} = A_{i j} - \frac{k_i k_j}{2 m},

    where *A* is the adjacency matrix, `k_i` is the degree of node *i*,
    and *m* is the number of edges in the graph. Nodes whose
    corresponding values in the eigenvector are negative are placed in
    one block, nodes whose values are nonnegative are placed in another
    block.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    C : tuple
        Pair of communities as two sets of nodes of ``G``, partitioned
        according to second largest eigenvalue of the modularity matrix.

    Examples
    --------
    >>> G = nx.karate_club_graph()
    >>> MrHi, Officer = nx.community.spectral_modularity_bipartition(G)
    >>> MrHi, Officer = sorted([sorted(MrHi), sorted(Officer)])
    >>> MrHi
    [0, 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 16, 17, 19, 21]
    >>> Officer
    [8, 9, 14, 15, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]

    References
    ----------
    .. [1] M. E. J. Newman *Networks: An Introduction*, pages 373--378
       Oxford University Press 2011.
    .. [2] M. E. J. Newman,
       "Modularity and community structure in networks",
       PNAS, 103 (23), p. 8577-8582,
       https://doi.org/10.1073/pnas.0601602103

    """
    import numpy as np

    B = nx.linalg.modularity_matrix(G)
    eigenvalues, eigenvectors = np.linalg.eig(B)
    index = np.argsort(eigenvalues)[-1]
    v2 = zip(np.real(eigenvectors[:, index]), G)
    left, right = set(), set()
    for u, n in v2:
        if u < 0:
            left.add(n)
        else:
            right.add(n)
    return left, right

