
def single(y):
    """
    Perform single/min/nearest linkage on the condensed distance matrix ``y``.

    Parameters
    ----------
    y : ndarray
        The upper triangular of the distance matrix. The result of
        ``pdist`` is returned in this form.

    Returns
    -------
    Z : ndarray
        The linkage matrix.

    See Also
    --------
    linkage : for advanced creation of hierarchical clusterings.
    scipy.spatial.distance.pdist : pairwise distance metrics

    Examples
    --------
    >>> from scipy.cluster.hierarchy import single, fcluster
    >>> from scipy.spatial.distance import pdist

    First, we need a toy dataset to play with::

        x x    x x
        x        x

        x        x
        x x    x x

    >>> X = [[0, 0], [0, 1], [1, 0],
    ...      [0, 4], [0, 3], [1, 4],
    ...      [4, 0], [3, 0], [4, 1],
    ...      [4, 4], [3, 4], [4, 3]]

    Then, we get a condensed distance matrix from this dataset:

    >>> y = pdist(X)

    Finally, we can perform the clustering:

    >>> Z = single(y)
    >>> Z
    array([[ 0.,  1.,  1.,  2.],
           [ 2., 12.,  1.,  3.],
           [ 3.,  4.,  1.,  2.],
           [ 5., 14.,  1.,  3.],
           [ 6.,  7.,  1.,  2.],
           [ 8., 16.,  1.,  3.],
           [ 9., 10.,  1.,  2.],
           [11., 18.,  1.,  3.],
           [13., 15.,  2.,  6.],
           [17., 20.,  2.,  9.],
           [19., 21.,  2., 12.]])

    The linkage matrix ``Z`` represents a dendrogram - see
    `scipy.cluster.hierarchy.linkage` for a detailed explanation of its
    contents.

    We can use `scipy.cluster.hierarchy.fcluster` to see to which cluster
    each initial point would belong given a distance threshold:

    >>> fcluster(Z, 0.9, criterion='distance')
    array([ 7,  8,  9, 10, 11, 12,  4,  5,  6,  1,  2,  3], dtype=int32)
    >>> fcluster(Z, 1, criterion='distance')
    array([3, 3, 3, 4, 4, 4, 2, 2, 2, 1, 1, 1], dtype=int32)
    >>> fcluster(Z, 2, criterion='distance')
    array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int32)

    Also, `scipy.cluster.hierarchy.dendrogram` can be used to generate a
    plot of the dendrogram.
    """
    return linkage(y, method='single', metric='euclidean')

