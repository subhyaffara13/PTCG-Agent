
def centroid(*args):
    """Find the centroid (center of mass) of the collection containing only Points,
    Segments or Polygons. The centroid is the weighted average of the individual centroid
    where the weights are the lengths (of segments) or areas (of polygons).
    Overlapping regions will add to the weight of that region.

    If there are no objects (or a mixture of objects) then None is returned.

    See Also
    ========

    sympy.geometry.point.Point, sympy.geometry.line.Segment,
    sympy.geometry.polygon.Polygon

    Examples
    ========

    >>> from sympy import Point, Segment, Polygon
    >>> from sympy.geometry.util import centroid
    >>> p = Polygon((0, 0), (10, 0), (10, 10))
    >>> q = p.translate(0, 20)
    >>> p.centroid, q.centroid
    (Point2D(20/3, 10/3), Point2D(20/3, 70/3))
    >>> centroid(p, q)
    Point2D(20/3, 40/3)
    >>> p, q = Segment((0, 0), (2, 0)), Segment((0, 0), (2, 2))
    >>> centroid(p, q)
    Point2D(1, 2 - sqrt(2))
    >>> centroid(Point(0, 0), Point(2, 0))
    Point2D(1, 0)

    Stacking 3 polygons on top of each other effectively triples the
    weight of that polygon:

    >>> p = Polygon((0, 0), (1, 0), (1, 1), (0, 1))
    >>> q = Polygon((1, 0), (3, 0), (3, 1), (1, 1))
    >>> centroid(p, q)
    Point2D(3/2, 1/2)
    >>> centroid(p, p, p, q) # centroid x-coord shifts left
    Point2D(11/10, 1/2)

    Stacking the squares vertically above and below p has the same
    effect:

    >>> centroid(p, p.translate(0, 1), p.translate(0, -1), q)
    Point2D(11/10, 1/2)

    """
    from .line import Segment
    from .polygon import Polygon
    if args:
        if all(isinstance(g, Point) for g in args):
            c = Point(0, 0)
            for g in args:
                c += g
            den = len(args)
        elif all(isinstance(g, Segment) for g in args):
            c = Point(0, 0)
            L = 0
            for g in args:
                l = g.length
                c += g.midpoint*l
                L += l
            den = L
        elif all(isinstance(g, Polygon) for g in args):
            c = Point(0, 0)
            A = 0
            for g in args:
                a = g.area
                c += g.centroid*a
                A += a
            den = A
        c /= den
        return c.func(*[i.simplify() for i in c.args])


def centroid(y):
    """
    Perform centroid/UPGMC linkage.

    See `linkage` for more information on the input matrix,
    return structure, and algorithm.

    The following are common calling conventions:

    1. ``Z = centroid(y)``

       Performs centroid/UPGMC linkage on the condensed distance
       matrix ``y``.

    2. ``Z = centroid(X)``

       Performs centroid/UPGMC linkage on the observation matrix ``X``
       using Euclidean distance as the distance metric.

    Parameters
    ----------
    y : ndarray
        A condensed distance matrix. A condensed
        distance matrix is a flat array containing the upper
        triangular of the distance matrix. This is the form that
        ``pdist`` returns. Alternatively, a collection of
        m observation vectors in n dimensions may be passed as
        an m by n array.

    Returns
    -------
    Z : ndarray
        A linkage matrix containing the hierarchical clustering. See
        the `linkage` function documentation for more information
        on its structure.

    See Also
    --------
    linkage : for advanced creation of hierarchical clusterings.
    scipy.spatial.distance.pdist : pairwise distance metrics

    Examples
    --------
    >>> from scipy.cluster.hierarchy import centroid, fcluster
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

    >>> Z = centroid(y)
    >>> Z
    array([[ 0.        ,  1.        ,  1.        ,  2.        ],
           [ 3.        ,  4.        ,  1.        ,  2.        ],
           [ 9.        , 10.        ,  1.        ,  2.        ],
           [ 6.        ,  7.        ,  1.        ,  2.        ],
           [ 2.        , 12.        ,  1.11803399,  3.        ],
           [ 5.        , 13.        ,  1.11803399,  3.        ],
           [ 8.        , 15.        ,  1.11803399,  3.        ],
           [11.        , 14.        ,  1.11803399,  3.        ],
           [18.        , 19.        ,  3.33333333,  6.        ],
           [16.        , 17.        ,  3.33333333,  6.        ],
           [20.        , 21.        ,  3.33333333, 12.        ]]) # may vary

    The linkage matrix ``Z`` represents a dendrogram - see
    `scipy.cluster.hierarchy.linkage` for a detailed explanation of its
    contents.

    We can use `scipy.cluster.hierarchy.fcluster` to see to which cluster
    each initial point would belong given a distance threshold:

    >>> fcluster(Z, 0.9, criterion='distance')
    array([ 7,  8,  9, 10, 11, 12,  1,  2,  3,  4,  5,  6], dtype=int32) # may vary
    >>> fcluster(Z, 1.1, criterion='distance')
    array([5, 5, 6, 7, 7, 8, 1, 1, 2, 3, 3, 4], dtype=int32) # may vary
    >>> fcluster(Z, 2, criterion='distance')
    array([3, 3, 3, 4, 4, 4, 1, 1, 1, 2, 2, 2], dtype=int32) # may vary
    >>> fcluster(Z, 4, criterion='distance')
    array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int32)

    Also, `scipy.cluster.hierarchy.dendrogram` can be used to generate a
    plot of the dendrogram.

    """
    return linkage(y, method='centroid', metric='euclidean')


def centroid(G):
    """Return the centroid of an unweighted tree.

    The centroid of a tree is the set of nodes such that removing any
    one of them would split the tree into a forest of subtrees, each
    with at most ``N / 2`` nodes, where ``N`` is the number of nodes
    in the original tree. This set may contain two nodes if removing
    an edge between them results in two trees of size exactly ``N /
    2``.

    Parameters
    ----------
    G : NetworkX graph
       A tree.

    Returns
    -------
    c : list
       List of nodes in centroid of the tree. This could be one or two nodes.

    Raises
    ------
    NotATree
        If the input graph is not a tree.
    NotImplementedException
        If the input graph is directed.
    NetworkXPointlessConcept
        If `G` has no nodes or edges.

    Notes
    -----
    This algorithm's time complexity is ``O(N)`` where ``N`` is the
    number of nodes in the tree.

    In unweighted trees the centroid coincides with the barycenter,
    the node or nodes that minimize the sum of distances to all other
    nodes. However, this concept is different from that of the graph
    center, which is the set of nodes minimizing the maximum distance
    to all other nodes.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.tree.centroid(G)
    [1, 2]

    A star-shaped tree with one long branch illustrates the difference
    between the centroid and the center. The center lies near the
    middle of the long branch, minimizing maximum distance. The
    centroid, however, limits the size of any resulting subtree to at
    most half the total nodes, forcing it to remain near the hub when
    enough short branches are present.

    >>> G = nx.star_graph(6)
    >>> nx.add_path(G, [6, 7, 8, 9, 10])
    >>> nx.tree.centroid(G), nx.tree.center(G)
    ([0], [7])

    See Also
    --------
    :func:`~networkx.algorithms.distance_measures.barycenter`
    :func:`~networkx.algorithms.distance_measures.center`
    center : tree center
    """
    if not nx.is_tree(G):
        raise nx.NotATree("provided graph is not a tree")
    prev, root = None, nx.utils.arbitrary_element(G)
    sizes = _subtree_sizes(G, root)
    total_size = G.number_of_nodes()

    def _heaviest_child(prev, root):
        return max(
            (x for x in G.neighbors(root) if x != prev), key=sizes.get, default=None
        )

    hc = _heaviest_child(prev, root)
    while max(total_size - sizes[root], sizes.get(hc, 0)) > total_size / 2:
        prev, root = root, hc
        hc = _heaviest_child(prev, root)

    return [root] + [
        x for x in G.neighbors(root) if x != prev and sizes[x] == total_size / 2
    ]

