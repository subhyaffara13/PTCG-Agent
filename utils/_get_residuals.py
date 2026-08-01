
def _get_residuals(x, y, t, k, w, periodic=False):
    # inline the relevant part of
    # >>> spl = make_lsq_spline(x, y, w=w2, t=t, k=k)
    # NB:
    #     1. y is assumed to be 2D here. For 1D case (parametric=False),
    #        the call must have been preceded by y = y[:, None] (cf _validate_inputs)
    #     2. We always sum the squares across axis=1:
    #         * For 1D (parametric=False), the last dimension has size one,
    #           so the summation is a no-op.
    #         * For 2D (parametric=True), the summation is actually how the
    #           'residuals' are defined, see Eq. (42) in Dierckx1982
    #           (the reference is in the docstring of `class F`) below.
    _, _, _, fp, residuals = _lsq_solve_qr(x, y, t, k, w, periodic=periodic)
    if np.isnan(residuals.sum()):
        raise ValueError(_iermesg[1])
    return residuals, fp

