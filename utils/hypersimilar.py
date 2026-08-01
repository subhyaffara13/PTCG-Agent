
def hypersimilar(f, g, k):
    """
    Returns True if ``f`` and ``g`` are hyper-similar.

    Explanation
    ===========

    Similarity in hypergeometric sense means that a quotient of
    f(k) and g(k) is a rational function in ``k``. This procedure
    is useful in solving recurrence relations.

    For more information see hypersimp().

    """
    f, g = list(map(sympify, (f, g)))

    h = (f/g).rewrite(gamma)
    h = h.expand(func=True, basic=False)

    return h.is_rational_function(k)

