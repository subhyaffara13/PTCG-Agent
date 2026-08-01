
def intersection_sets(self, o): # noqa:F811
    """ Returns a sympy.sets.Set of intersection objects,
    if possible. """

    from sympy.geometry.point import Point

    try:
        # if o is a FiniteSet, find the intersection directly
        # to avoid infinite recursion
        if o.is_FiniteSet:
            inter = FiniteSet(*(p for p in o if self.contains(p)))
        else:
            inter = self.intersection(o)
    except NotImplementedError:
        # sympy.sets.Set.reduce expects None if an object
        # doesn't know how to simplify
        return None

    # put the points in a FiniteSet
    points = FiniteSet(*[p for p in inter if isinstance(p, Point)])
    non_points = [p for p in inter if not isinstance(p, Point)]

    return Union(*(non_points + [points]))

