
def res(f, g, x):
    """
    The input polynomials f, g are in Z[x] or in Q[x].

    The output is the resultant of f, g computed by evaluating
    the determinant of the matrix sylvester(f, g, x, 1).

    References:
    ===========
    1. J. S. Cohen: Computer Algebra and Symbolic Computation
     - Mathematical Methods. A. K. Peters, 2003.

    """
    if f == 0 or g == 0:
        raise PolynomialError("The resultant of %s and %s is not defined" % (f, g))
    else:
        return sylvester(f, g, x, 1).det()

