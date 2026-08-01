
def is_vertex(ent):
    """If the input entity is a vertex return True.

    Parameter
    =========

    ent :
        Denotes a geometric entity representing a point.

    Examples
    ========

    >>> from sympy import Point
    >>> from sympy.integrals.intpoly import is_vertex
    >>> is_vertex((2, 3))
    True
    >>> is_vertex((2, 3, 6))
    True
    >>> is_vertex(Point(2, 3))
    True
    """
    if isinstance(ent, tuple):
        if len(ent) in [2, 3]:
            return True
    elif isinstance(ent, Point):
        return True
    return False

