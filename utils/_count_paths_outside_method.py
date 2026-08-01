
def _count_paths_outside_method(m, n, g, h):
    """Count the number of paths that pass outside the specified diagonal.

    Parameters
    ----------
    m : int
        m > 0
    n : int
        n > 0
    g : int
        g is greatest common divisor of m and n
    h : int
        0 <= h <= lcm(m,n)

    Returns
    -------
    p : float
        The number of paths that go low.
        The calculation may overflow - check for a finite answer.

    Notes
    -----
    Count the integer lattice paths from (0, 0) to (m, n), which at some
    point (x, y) along the path, satisfy:
      m*y <= n*x - h*g
    The paths make steps of size +1 in either positive x or positive y
    directions.

    We generally follow Hodges' treatment of Drion/Gnedenko/Korolyuk.
    Hodges, J.L. Jr.,
    "The Significance Probability of the Smirnov Two-Sample Test,"
    Arkiv fiur Matematik, 3, No. 43 (1958), 469-86.

    """
    # Compute #paths which stay lower than x/m-y/n = h/lcm(m,n)
    # B(x, y) = #{paths from (0,0) to (x,y) without
    #             previously crossing the boundary}
    #         = binom(x, y) - #{paths which already reached the boundary}
    # Multiply by the number of path extensions going from (x, y) to (m, n)
    # Sum.

    # Probability is symmetrical in m, n.  Computation below assumes m >= n.
    if m < n:
        m, n = n, m
    mg = m // g
    ng = n // g

    # Not every x needs to be considered.
    # xj holds the list of x values to be checked.
    # Wherever n*x/m + ng*h crosses an integer
    lxj = n + (mg-h)//mg
    xj = [(h + mg * j + ng-1)//ng for j in range(lxj)]
    # B is an array just holding a few values of B(x,y), the ones needed.
    # B[j] == B(x_j, j)
    if lxj == 0:
        return special.binom(m + n, n)
    B = np.zeros(lxj)
    B[0] = 1
    # Compute the B(x, y) terms
    for j in range(1, lxj):
        Bj = special.binom(xj[j] + j, j)
        for i in range(j):
            bin = special.binom(xj[j] - xj[i] + j - i, j-i)
            Bj -= bin * B[i]
        B[j] = Bj
    # Compute the number of path extensions...
    num_paths = 0
    for j in range(lxj):
        bin = special.binom((m-xj[j]) + (n - j), n-j)
        term = B[j] * bin
        num_paths += term
    return num_paths

