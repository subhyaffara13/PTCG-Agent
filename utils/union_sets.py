from typing import Union

def union_sets(self, o): # noqa:F811
    """ Returns the union of self and o
    for use with sympy.sets.Set, if possible. """


    # if its a FiniteSet, merge any points
    # we contain and return a union with the rest
    if o.is_FiniteSet:
        other_points = [p for p in o if not self._contains(p)]
        if len(other_points) == len(o):
            return None
        return Union(self, FiniteSet(*other_points))
    if self._contains(o):
        return self
    return None

