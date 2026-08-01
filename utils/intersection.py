
def intersection(*entities, pairwise=False, **kwargs):
    """The intersection of a collection of GeometryEntity instances.

    Parameters
    ==========
    entities : sequence of GeometryEntity
    pairwise (keyword argument) : Can be either True or False

    Returns
    =======
    intersection : list of GeometryEntity

    Raises
    ======
    NotImplementedError
        When unable to calculate intersection.

    Notes
    =====
    The intersection of any geometrical entity with itself should return
    a list with one item: the entity in question.
    An intersection requires two or more entities. If only a single
    entity is given then the function will return an empty list.
    It is possible for `intersection` to miss intersections that one
    knows exists because the required quantities were not fully
    simplified internally.
    Reals should be converted to Rationals, e.g. Rational(str(real_num))
    or else failures due to floating point issues may result.

    Case 1: When the keyword argument 'pairwise' is False (default value):
    In this case, the function returns a list of intersections common to
    all entities.

    Case 2: When the keyword argument 'pairwise' is True:
    In this case, the functions returns a list intersections that occur
    between any pair of entities.

    See Also
    ========

    sympy.geometry.entity.GeometryEntity.intersection

    Examples
    ========

    >>> from sympy import Ray, Circle, intersection
    >>> c = Circle((0, 1), 1)
    >>> intersection(c, c.center)
    []
    >>> right = Ray((0, 0), (1, 0))
    >>> up = Ray((0, 0), (0, 1))
    >>> intersection(c, right, up)
    [Point2D(0, 0)]
    >>> intersection(c, right, up, pairwise=True)
    [Point2D(0, 0), Point2D(0, 2)]
    >>> left = Ray((1, 0), (0, 0))
    >>> intersection(right, left)
    [Segment2D(Point2D(0, 0), Point2D(1, 0))]

    """
    if len(entities) <= 1:
        return []

    entities = list(entities)
    prec = None
    for i, e in enumerate(entities):
        if not isinstance(e, GeometryEntity):
            # entities may be an immutable tuple
            e = Point(e)
        # convert to exact Rationals
        d = {}
        for f in e.atoms(Float):
            prec = f._prec if prec is None else min(f._prec, prec)
            d.setdefault(f, nsimplify(f, rational=True))
        entities[i] = e.xreplace(d)

    if not pairwise:
        # find the intersection common to all objects
        res = entities[0].intersection(entities[1])
        for entity in entities[2:]:
            newres = []
            for x in res:
                newres.extend(x.intersection(entity))
            res = newres
    else:
        # find all pairwise intersections
        ans = []
        for j in range(len(entities)):
            for k in range(j + 1, len(entities)):
                ans.extend(intersection(entities[j], entities[k]))
        res = list(ordered(set(ans)))

    # convert back to Floats
    if prec is not None:
        p = prec_to_dps(prec)
        res = [i.n(p) for i in res]
    return res


def intersection(geom_1, geom_2, intersection_type):
    """Returns intersection between geometric objects.

    Explanation
    ===========

    Note that this function is meant for use in integration_reduction and
    at that point in the calling function the lines denoted by the segments
    surely intersect within segment boundaries. Coincident lines are taken
    to be non-intersecting. Also, the hyperplane intersection for 2D case is
    also implemented.

    Parameters
    ==========

    geom_1, geom_2:
        The input line segments.

    Examples
    ========

    >>> from sympy.integrals.intpoly import intersection
    >>> from sympy import Point, Segment2D
    >>> l1 = Segment2D(Point(1, 1), Point(3, 5))
    >>> l2 = Segment2D(Point(2, 0), Point(2, 5))
    >>> intersection(l1, l2, "segment2D")
    (2, 3)
    >>> p1 = ((-1, 0), 0)
    >>> p2 = ((0, 1), 1)
    >>> intersection(p1, p2, "plane2D")
    (0, 1)
    """
    if intersection_type[:-2] == "segment":
        if intersection_type == "segment2D":
            x1, y1 = geom_1.points[0]
            x2, y2 = geom_1.points[1]
            x3, y3 = geom_2.points[0]
            x4, y4 = geom_2.points[1]
        elif intersection_type == "segment3D":
            x1, y1, z1 = geom_1.points[0]
            x2, y2, z2 = geom_1.points[1]
            x3, y3, z3 = geom_2.points[0]
            x4, y4, z4 = geom_2.points[1]

        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denom:
            t1 = x1 * y2 - y1 * x2
            t2 = x3 * y4 - x4 * y3
            return (S(t1 * (x3 - x4) - t2 * (x1 - x2)) / denom,
                    S(t1 * (y3 - y4) - t2 * (y1 - y2)) / denom)
    if intersection_type[:-2] == "plane":
        if intersection_type == "plane2D":  # Intersection of hyperplanes
            a1x, a1y = geom_1[0]
            a2x, a2y = geom_2[0]
            b1, b2 = geom_1[1], geom_2[1]

            denom = a1x * a2y - a2x * a1y
            if denom:
                return (S(b1 * a2y - b2 * a1y) / denom,
                        S(b2 * a1x - b1 * a2x) / denom)


def intersection(G, H):
    """Returns a new graph that contains only the nodes and the edges that exist in
    both G and H.

    Parameters
    ----------
    G,H : graph
       A NetworkX graph. G and H can have different node sets but must be both graphs or both multigraphs.

    Raises
    ------
    NetworkXError
        If one is a MultiGraph and the other one is a graph.

    Returns
    -------
    GH : A new graph with the same type as G.

    Notes
    -----
    Attributes from the graph, nodes, and edges are not copied to the new
    graph.  If you want a new graph of the intersection of G and H
    with the attributes (including edge data) from G use remove_nodes_from()
    as follows

    >>> G = nx.path_graph(3)
    >>> H = nx.path_graph(5)
    >>> R = G.copy()
    >>> R.remove_nodes_from(n for n in G if n not in H)
    >>> R.remove_edges_from(e for e in G.edges if e not in H.edges)

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (1, 2)])
    >>> H = nx.Graph([(0, 3), (1, 2), (2, 3)])
    >>> R = nx.intersection(G, H)
    >>> R.nodes
    NodeView((0, 1, 2))
    >>> R.edges
    EdgeView([(1, 2)])
    """
    return nx.intersection_all([G, H])

