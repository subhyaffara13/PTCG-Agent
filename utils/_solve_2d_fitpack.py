
def _solve_2d_fitpack(Ax, Ay, Q, p,
                      kx, tx, x_x,
                      ky, ty, x_y, z,
                      Dx=None, Dy=None):
    """
    Solve the 2-D tensor-product spline system using separable banded QR.

    ================================================================
    Mathematical model (step by step, plain text)
    ================================================================

    Shapes:
        Z      : (mx, my)  -> original data
        Ax, Ay : design matrices for x and y
        Dx, Dy : roughness penalty matrices for x and y
        C      : (nx, ny)  -> spline coefficients to solve for

    Surface approximation:
        Zhat = Ax * C * Ay^T

    Objective (smoothing formulation):
        minimize ||Ax*C*Ay^T - Z||^2 + (1/p)*(||Dx*C||^2 + ||C*Dy^T||^2)

    In practice (FITPACK-style separable approach), we solve this in two stages:

    --------------------------------------------------------
    Stage 1 (x-direction solve for all y-columns together):
    --------------------------------------------------------

        For each column of Z:
            minimize ||Ax*T - Z||^2 + (1/p)*||Dx*T||^2

        This is equivalent to the augmented least-squares system:
            [Ax]       [Z]
            [Dx/p] * T = [0]

        i.e.  minimize || [Ax; Dx/p]*T - [Z; 0] ||^2

        The solution T is obtained by QR reduction and back-substitution.

    --------------------------------------------------------
    Stage 2 (y-direction solve using transposed result):
    --------------------------------------------------------
        Now treat T^T as the new RHS for the y-direction:
            minimize ||Ay*C^T - T^T||^2 + (1/p)*||Dy*C^T||^2

        Equivalent to augmented system:
            [Ay]       [T^T]
            [Dy/p] * C^T = [0]

        i.e.  minimize || [Ay; Dy/p]*C^T - [T^T; 0] ||^2

        Solving this gives C^T (then transposed back to C).

    --------------------------------------------------------
    Interpolation limit:
    --------------------------------------------------------
        If p == -1, penalties are omitted (Dx, Dy are not stacked).
        The solver behaves as a near-interpolating system.

    --------------------------------------------------------
    Residual computation:
    --------------------------------------------------------
        Zhat = Ax * C * Ay^T
        R    = Z - Zhat
        fp   = sum(R^2)

    Parameters
    ----------
    Ax, Ay : PackedMatrix
        Banded data matrices for the x and y axes.
    Q : ndarray, shape (mx, my)
        RHS data grid (copied from `Z`).
    p : float
        Smoothing parameter. The penalty term is scaled as **1/p**.
        Setting `p == -1` signals *p -> inf* (interpolation, omit penalty).
    kx, ky : int
        Spline degrees along x and y.
    tx, ty : ndarray
        Knot vectors along x and y.
    x_x, x_y : ndarray
        Sample coordinates.
    z : ndarray
        Original data grid for residual evaluation.
    Dx, Dy : ndarray
        Banded roughness penalty matrices for x and y.
        Optional, Only needed when ``p != -1``.

    Returns
    -------
    C : ndarray
        2-D B-spline coefficient grid.
    fp : float
        Residual sum of squares between fitted surface and `z`.
    R : ndarray, shape (mx, my)
        Residual matrix ``z - zhat``, where ``zhat = Ax @ C @ Ay.T``.

    Notes
    -----
    This performs two separable QR solves (x then y), each augmented by
    `(D / p)` when `p != -1`.  Setting `p = -1` skips all penalty rows,
    yielding an interpolatory surface.  The resulting coefficients and residual
    follow the same conventions as FITPACK's `fpgrre`.
    """
    # Dummy unit weights for FITPACK fpback APIs.
    w_x = np.ones_like(x_x)
    w_y = np.ones_like(x_y)

    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L97-L105
    # Build the augmented banded matrix for x:
    #   - If p != -1, stack (Dx / p) under Ax for FITPACK-style smoothing.
    #   - If p == -1, _stack_augmented_fitpack omits the penalty part entirely.
    # Returns:
    #   Ax_aug      : augmented banded matrix (data [+ penalty]).
    #   offset_aug_x: band offsets compatible with Ax_aug.
    #   nc_augx     : number of top data rows within Ax_aug (== ncx).
    Ax_aug, offset_aug_x, nc_augx = _stack_augmented_fitpack(
        Ax, Dx, Ax.shape[0], kx, p)
    nc_x = Ax.nc

    # Same for y: build Ay_aug with (Dy / p) stacked if p != -1.
    Ay_aug, offset_aug_y, nc_augy = _stack_augmented_fitpack(
        Ay, Dy, Ay.shape[0], ky, p)
    nc_y = Ay.nc

    # If we stacked penalty rows on the x side, the RHS must be padded with zeros
    # to match the augmented row count for the QR reduction call.
    if p != -1: # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L97
        # Dx.shape[0] is the number of penalty rows; add that many zero rows
        # so Ax_aug and Q have compatible leading dimensions for in-place QR.
        # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L110-L118
        Q = np.vstack([Q, np.zeros((Dx.shape[0], Q.shape[1]), dtype=float)])

    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L106-L175
    # Perform in-place banded QR reduction of the x-augmented system:
    # This orthogonalizes/eliminates along x for all RHS columns in Q simultaneously.
    # After this, fpback can do x-direction back-substitution to
    # get c^T (partial coeffs).
    _dierckx.qr_reduce(Ax_aug, offset_aug_x, nc_augx, Q)

    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L246-L253
    # Back-substitute along x to solve the reduced system:
    #   cT has shape (ncoef_x, num_y_data) in this calling pattern, i.e. per y-column.
    # The API uses:
    #   Ax_aug, nc_augx: reduced upper structure
    #   x_x, tx, kx, w_x: x-sample grid, knot vector, degree, and (unit) weights
    #   Q: RHS (current)
    # fpback returns shape (nc_x, num_y_data)
    T, _, _ = _dierckx.fpback(
        Ax_aug, nc_x, x_x,
        Q, tx, kx, w_x,
        Q, False
    )

    # We now want to treat the *y*-direction solve with these as the new RHS.
    # Transpose so each column corresponds to a y-solve RHS consistently.
    Q = np.ascontiguousarray(T.T)

    # If we stacked penalty rows on the y side, pad RHS with zeros to match Ay_aug.
    if p != -1: # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L97
        # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L110-L118
        Q = np.vstack([Q, np.zeros((Dy.shape[0], Q.shape[1]), dtype=float)])

    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L176-L245
    # Perform in-place banded QR reduction along y for all columns of Q.
    _dierckx.qr_reduce(Ay_aug, offset_aug_y, nc_augy, Q)

    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpgrre.f#L254-L269
    # Final back-substitution along y:
    # Returns:
    #   C  : coefficient matrix with shape (nc_y, nc_x)
    #   fp : FITPACK's internal residual metric from the y-solve
    #        (we recompute below anyway)
    C, _, fp = _dierckx.fpback(
        Ay_aug, nc_y,
        x_y, Q, ty, ky, w_y,    # y-grid, y-knots, degree, weights
        Q,                      # RHS -> solution becomes coefficients along y
        False
    )

    # Build explicit design matrices to evaluate the fitted surface:
    # _Ax: [mx × nx_coef], _Ay: [my × ny_coef]
    # Note: We call PackedMatrix.tocsr here because matrix multiplication
    # with the packed banded format (returned by _dierckx.data_matrix)
    # is not implemented. PackedMatrix.tocsr returns the design matrix,
    # in CSR format, that supports standard @ operations for residual
    # evaluation and diagnostics.
    _Ax = Ax.tocsr(kx, x_x.shape[0], len(tx))
    _Ay = Ay.tocsr(ky, x_y.shape[0], len(ty))

    # Evaluate the fitted surface: zhat = Ax * C^T * Ay^T
    # Note: C currently aligns so that C.T matches x-first multiplication order.
    zhat = _Ax @ C.T @ _Ay.T

    # Compute residual matrix R and fp in one pass; return R so callers that
    # need per-span energy for knot placement can reuse it directly instead of
    # recomputing zhat a second time.
    R = z - zhat
    fp = np.sum(np.square(R))

    # Return coefficients in the conventional (nx_coef, ny_coef) orientation,
    # fp, and the residual matrix R.
    return C.T, fp, R

