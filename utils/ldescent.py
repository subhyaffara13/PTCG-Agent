
def ldescent(A, B):
    """
    Return a non-trivial solution to `w^2 = Ax^2 + By^2` using
    Lagrange's method; return None if there is no such solution.

    Parameters
    ==========

    A : Integer
    B : Integer
        non-zero integer

    Returns
    =======

    (int, int, int) | None : a tuple `(w_0, x_0, y_0)` which is a solution to the above equation.

    Examples
    ========

    >>> from sympy.solvers.diophantine.diophantine import ldescent
    >>> ldescent(1, 1) # w^2 = x^2 + y^2
    (1, 1, 0)
    >>> ldescent(4, -7) # w^2 = 4x^2 - 7y^2
    (2, -1, 0)

    This means that `x = -1, y = 0` and `w = 2` is a solution to the equation
    `w^2 = 4x^2 - 7y^2`

    >>> ldescent(5, -1) # w^2 = 5x^2 - y^2
    (2, 1, -1)

    References
    ==========

    .. [1] The algorithmic resolution of Diophantine equations, Nigel P. Smart,
           London Mathematical Society Student Texts 41, Cambridge University
           Press, Cambridge, 1998.
    .. [2] Cremona, J. E., Rusin, D. (2003). Efficient Solution of Rational Conics.
           Mathematics of Computation, 72(243), 1417-1441.
           https://doi.org/10.1090/S0025-5718-02-01480-1
    """
    if A == 0 or B == 0:
        raise ValueError("A and B must be non-zero integers")
    if abs(A) > abs(B):
        w, y, x = ldescent(B, A)
        return w, x, y
    if A == 1:
        return (1, 1, 0)
    if B == 1:
        return (1, 0, 1)
    if B == -1:  # and A == -1
        return

    r = sqrt_mod(A, B)
    if r is None:
        return
    Q = (r**2 - A) // B
    if Q == 0:
        return r, -1, 0
    for i in divisors(Q):
        d, _exact = integer_nthroot(abs(Q) // i, 2)
        if _exact:
            B_0 = sign(Q)*i
            W, X, Y = ldescent(A, B_0)
            return _remove_gcd(-A*X + r*W, r*X - W, Y*B_0*d)

