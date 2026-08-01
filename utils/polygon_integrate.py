
def polygon_integrate(facet, hp_param, index, facets, vertices, expr, degree):
    """Helper function to integrate the input uni/bi/trivariate polynomial
    over a certain face of the 3-Polytope.

    Parameters
    ==========

    facet :
        Particular face of the 3-Polytope over which ``expr`` is integrated.
    index :
        The index of ``facet`` in ``facets``.
    facets :
        Faces of the 3-Polytope(expressed as indices of `vertices`).
    vertices :
        Vertices that constitute the facet.
    expr :
        The input polynomial.
    degree :
        Degree of ``expr``.

    Examples
    ========

    >>> from sympy.integrals.intpoly import polygon_integrate
    >>> cube = [[(0, 0, 0), (0, 0, 5), (0, 5, 0), (0, 5, 5), (5, 0, 0),\
                 (5, 0, 5), (5, 5, 0), (5, 5, 5)],\
                 [2, 6, 7, 3], [3, 7, 5, 1], [7, 6, 4, 5], [1, 5, 4, 0],\
                 [3, 1, 0, 2], [0, 4, 6, 2]]
    >>> facet = cube[1]
    >>> facets = cube[1:]
    >>> vertices = cube[0]
    >>> polygon_integrate(facet, [(0, 1, 0), 5], 0, facets, vertices, 1, 0)
    -25
    """
    expr = S(expr)
    if expr.is_zero:
        return S.Zero
    result = S.Zero
    x0 = vertices[facet[0]]
    facet_len = len(facet)
    for i, fac in enumerate(facet):
        side = (vertices[fac], vertices[facet[(i + 1) % facet_len]])
        result += distance_to_side(x0, side, hp_param[0]) *\
            lineseg_integrate(facet, i, side, expr, degree)
    if not expr.is_number:
        expr = diff(expr, x) * x0[0] + diff(expr, y) * x0[1] +\
            diff(expr, z) * x0[2]
        result += polygon_integrate(facet, hp_param, index, facets, vertices,
                                    expr, degree - 1)
    result /= (degree + 2)
    return result

