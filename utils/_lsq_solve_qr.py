
def _lsq_solve_qr(x, y, t, k, w, periodic=False):
    """Solve for the LSQ spline coeffs given x, y and knots.

    `y` is always 2D: for 1D data, the shape is ``(m, 1)``.
    `w` is always 1D: one weight value per `x` value.

    """
    y_w = y * w[:, None]
    if not periodic:
        A, offset, nc = _dierckx.data_matrix(x, t, k, w)
        _dierckx.qr_reduce(A, offset, nc, y_w)         # modifies arguments in-place
        c, residuals, fp = _dierckx.fpback(A, nc, x, y, t, k, w, y_w)
        return A, y_w, c, fp, residuals
    else:
        # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L221-L238
        R, H1, H2, offset, nc = _dierckx.data_matrix_periodic(x, t, k, w, False)
        # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L239-L314
        A1, A2, Z, fp = _dierckx.qr_reduce_periodic(
            R, H1, H2, offset, nc, y_w, k,
            len(t), False)         # modifies arguments in-place
        # Ref: https://github.com/scipy/scipy/blob/main/scipy/interpolate/fitpack/fpbacp.f
        c, residuals, _ = _dierckx.fpbacp(A1, A2, Z, k, k, x, y, t, w)
        return R, y_w, c, fp, residuals

