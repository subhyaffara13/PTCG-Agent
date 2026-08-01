
def _initialise_knots(m, xb, xe, k, nest=None):
    """
    Initialize a non-periodic knot vector.

    Parameters
    ----------
    m : int
        Number of data points (equivalent to len(x) if x were provided).
    xb, xe : float
        Domain endpoints used to seed the initial knot vector with no internal knots.
    k : int
        Spline degree.
    nest : int, optional
        Storage cap for knots. If None, defaults to max(m + k + 1, 2*k + 3).
        Must satisfy nest >= 2*(k + 1); otherwise a ValueError is raised.

    Returns
    -------
    t : 1-D ndarray
        Initial knot vector with no internal knots: [xb]*(k+1) + [xe]*(k+1).
    nest : int
        The finalized storage cap for knots.
    nmin : int
        Lower bound on knot count.
    nmax : int
        Upper bound on knot count.

    What this does
    --------------
    - Computes defaults and bounds used by FITPACK-style knot growth:
        * nest: storage cap for knots (defaults to max(m + k + 1, 2*k + 3))
        * nmin: minimal knot count (2*(k+1))
        * nmax: maximal knot count (m + k + 1)
    - Returns an initial knot vector with no internal knots:
        t = [xb]*(k+1) + [xe]*(k+1)
    """
    if nest is None:
        nest = max(m + k + 1, 2*k + 3)
    else:
        if nest < 2*(k + 1):
            raise ValueError(f"`nest` too small: {nest = } < 2*(k+1) = {2*(k+1)}.")

    nmin = 2*(k + 1)    # the number of knots for an LSQ polynomial approximation
    nmax = m + k + 1  # the number of knots for the spline interpolation

    # start from no internal knots
    t = np.asarray([xb]*(k+1) + [xe]*(k+1))

    return t, nest, nmin, nmax

