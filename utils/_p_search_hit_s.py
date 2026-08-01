
def _p_search_hit_s(
    Ax, Dx, Ay, Dy, Q, kx,
    tx, x_x, ky, ty, x_y, z, s, fp0, *,
    p_init=1.0, tol_rel=1e-3, maxit=40):
    """
    Search for a smoothing parameter `p` such that `fp(p) ~ s`.

    Parameters
    ----------
    Ax, Ay : PackedMatrix
        Banded data matrices.
    Dx, Dy : PackedMatrix
        Banded penalty matrices.
    Q : ndarray
        RHS data grid (copy of `Z`).
    kx, ky : int
        Spline degrees.
    tx, ty : ndarray
        Knot vectors.
    x_x, x_y : ndarray
        Sample coordinates.
    w_x, w_y : ndarray
        Sample weights.
    z : ndarray
        Original data grid for residuals.
    s : float
        Target smoothing residual (`fp` target).
    fp0 : float or None
        Residual at `p = inf` (interpolatory limit,
                               represented by `p == -1`).
    p_init : float, optional
        Starting guess for the finite `p` search, default 1.0.
    tol_rel : float, optional
        Relative tolerance for matching `fp(p)` to `s`.
    maxit : int, optional
        Maximum iterations for the root search.

    Returns
    -------
    p_star : float
        Smoothing parameter for which `fp(p_star)` ~ `s`.
    C_star : ndarray
        Coefficient grid corresponding to `p_star`.
    fp_star : float
        Residual at `p_star`.

    Notes
    -----
    The solver treats `p == -1` as *p = inf* (interpolatory, no penalty).
    For finite `p`, the penalty scales as **1/p** - smaller `p` increases
    smoothing. A ratio-of-roots search (`root_rati`) iteratively adjusts `p`
    until the residual `fp(p)` matches the target `s` within tolerance.
    """

    fp_at = F(Ax, Dx, Ay, Dy, Q, kx,
              tx, x_x, ky, ty, x_y, z)

    def g(p):
        return fp_at(p) - s

    fpms = g(-1)

    bracket = ((0.0, fp0 - s), (np.inf, fpms))
    ftol = max(s * tol_rel, 1e-12)

    r = root_rati(g, p_init, bracket, ftol, maxit=maxit)
    p_star = r.root
    fp_star = fp_at(p_star)
    C_star = fp_at.C

    return p_star, C_star, fp_star

