
def res_q(f, g, x):
    """
    The input polynomials f, g are in Z[x] or in Q[x].

    The output is the resultant of f, g computed recursively
    by polynomial divisions in Q[x], using the function rem.
    See Cohen's book p. 281.

    References:
    ===========
    1. J. S. Cohen: Computer Algebra and Symbolic Computation
     - Mathematical Methods. A. K. Peters, 2003.
    """
    m = degree(f, x)
    n = degree(g, x)
    if m < n:
        return (-1)**(m*n) * res_q(g, f, x)
    elif n == 0:  # g is a constant
        return g**m
    else:
        r = rem(f, g, x)
        if r == 0:
            return 0
        else:
            s = degree(r, x)
            l = LC(g, x)
            return (-1)**(m*n) * l**(m-s)*res_q(g, r, x)

