
def _imag_count_of_factor(f):
    """Return the number of imaginary roots for irreducible
    univariate polynomial ``f``.
    """
    terms = [(i, j) for (i,), j in f.terms()]
    if any(i % 2 for i, j in terms):
        return 0
    # update signs
    even = [(i, I**i*j) for i, j in terms]
    even = Poly.from_dict(dict(even), Dummy('x'))
    return int(even.count_roots(-oo, oo))

