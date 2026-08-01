
def _nolan_round_x_near_zeta(x0, alpha, zeta, x_tol_near_zeta):
    """Round x close to zeta for Nolan's method in [NO]."""
    #   "8. When |x0-beta*tan(pi*alpha/2)| is small, the
    #   computations of the density and cumulative have numerical problems.
    #   The program works around this by setting
    #   z = beta*tan(pi*alpha/2) when
    #   |z-beta*tan(pi*alpha/2)| < tol(5)*alpha**(1/alpha).
    #   (The bound on the right is ad hoc, to get reasonable behavior
    #   when alpha is small)."
    # where tol(5) = 0.5e-2 by default.
    #
    # We seem to have partially addressed this through re-expression of
    # g(theta) here, but it still needs to be used in some extreme cases.
    # Perhaps tol(5) = 0.5e-2 could be reduced for our implementation.
    if np.abs(x0 - zeta) < x_tol_near_zeta * alpha ** (1 / alpha):
        x0 = zeta
    return x0

