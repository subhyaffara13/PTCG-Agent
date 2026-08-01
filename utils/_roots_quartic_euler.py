
def _roots_quartic_euler(p, q, r, a):
    """
    Descartes-Euler solution of the quartic equation

    Parameters
    ==========

    p, q, r: coefficients of ``x**4 + p*x**2 + q*x + r``
    a: shift of the roots

    Notes
    =====

    This is a helper function for ``roots_quartic``.

    Look for solutions of the form ::

      ``x1 = sqrt(R) - sqrt(A + B*sqrt(R))``
      ``x2 = -sqrt(R) - sqrt(A - B*sqrt(R))``
      ``x3 = -sqrt(R) + sqrt(A - B*sqrt(R))``
      ``x4 = sqrt(R) + sqrt(A + B*sqrt(R))``

    To satisfy the quartic equation one must have
    ``p = -2*(R + A); q = -4*B*R; r = (R - A)**2 - B**2*R``
    so that ``R`` must satisfy the Descartes-Euler resolvent equation
    ``64*R**3 + 32*p*R**2 + (4*p**2 - 16*r)*R - q**2 = 0``

    If the resolvent does not have a rational solution, return None;
    in that case it is likely that the Ferrari method gives a simpler
    solution.

    Examples
    ========

    >>> from sympy import S
    >>> from sympy.polys.polyroots import _roots_quartic_euler
    >>> p, q, r = -S(64)/5, -S(512)/125, -S(1024)/3125
    >>> _roots_quartic_euler(p, q, r, S(0))[0]
    -sqrt(32*sqrt(5)/125 + 16/5) + 4*sqrt(5)/5
    """
    # solve the resolvent equation
    x = Dummy('x')
    eq = 64*x**3 + 32*p*x**2 + (4*p**2 - 16*r)*x - q**2
    xsols = list(roots(Poly(eq, x), cubics=False).keys())
    xsols = [sol for sol in xsols if sol.is_rational and sol.is_nonzero]
    if not xsols:
        return None
    R = max(xsols)
    c1 = sqrt(R)
    B = -q*c1/(4*R)
    A = -R - p/2
    c2 = sqrt(A + B)
    c3 = sqrt(A - B)
    return [c1 - c2 - a, -c1 - c3 - a, -c1 + c3 - a, c1 + c2 - a]

