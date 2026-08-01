
def _lsq_solve_qr_for_root_rati_periodic(x, y, t, k, w):
    """Solve for the LSQ spline coeffs given x, y and knots.

    `y` is always 2D: for 1D data, the shape is ``(m, 1)``.
    `w` is always 1D: one weight value per `x` value.

    """
    y_w = y * w[:, None]
    # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L221-L238
    R, H1, H2, offset, nc = _dierckx.data_matrix_periodic(x, t, k, w, False)
    # Ref: https://github.com/scipy/scipy/blob/maintenance/1.16.x/scipy/interpolate/fitpack/fpperi.f#L239-L314
    A1, A2, Z, p, _ = _dierckx.qr_reduce_periodic(
        R, H1, H2, offset, nc, y_w, k,
        len(t), True
    )         # modifies arguments in-place
    # Ref: https://github.com/scipy/scipy/blob/main/scipy/interpolate/fitpack/fpbacp.f
    c, residuals, _ = _dierckx.fpbacp(A1, A2, Z, k, k, x, y, t, w)
    return R, A1, A2, Z, y_w, c, p, residuals

