
def res_z(f, g, x):
    """
    The input polynomials f, g are in Z[x] or in Q[x].

    The output is the resultant of f, g computed recursively
    by polynomial divisions in Z[x], using the function prem().
    See Cohen's book p. 283.

    References:
    ===========
    1. J. S. Cohen: Computer Algebra and Symbolic Computation
     - Mathematical Methods. A. K. Peters, 2003.
    """
    m = degree(f, x)
    n = degree(g, x)
    if m < n:
        return (-1)**(m*n) * res_z(g, f, x)
    elif n == 0:  # g is a constant
        return g**m
    else:
        r = prem(f, g, x)
        if r == 0:
            return 0
        else:
            delta = m - n + 1
            w = (-1)**(m*n) * res_z(g, r, x)
            s = degree(r, x)
            l = LC(g, x)
            k = delta * n - m + s
            return quo(w, l**k, x)

