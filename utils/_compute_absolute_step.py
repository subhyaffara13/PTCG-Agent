
def _compute_absolute_step(rel_step, x0, f0, method):
    """
    Computes an absolute step from a relative step for finite difference
    calculation.

    Parameters
    ----------
    rel_step: None or array-like
        Relative step for the finite difference calculation
    x0 : np.ndarray
        Parameter vector
    f0 : np.ndarray or scalar
    method : {'2-point', '3-point', 'cs'}

    Returns
    -------
    h : np.array
        The absolute step size, ``h.dtype==x0.dtype``.

    Notes
    -----
    `h` has the same dtype as `x0` because dx is later calculated
    as ``(x0 + h) - x0``, and problems would occur if ``x0.dtype==np.float16``
    with ``h.dtype==np.float64``.
    If `rel_step is None`, then a default relative step is calculated using the
    smallest floating point type of `x0` and `f0`, see _eps_for_method.

    """
    # this is used instead of np.sign(x0) because we need
    # sign_x0 to be 1 when x0 == 0.
    sign_x0 = (x0 >= 0).astype(x0.dtype) * 2 - 1

    rstep = _eps_for_method(x0.dtype, f0.dtype, method)
    default_abs_step = (
        rstep * sign_x0 * np.maximum(1.0, np.abs(x0))
    ).astype(x0.dtype)

    if rel_step is None:
        abs_step = default_abs_step
    else:
        # User has requested specific relative steps.
        # Don't multiply by max(1, abs(x0) because if x0 < 1 then their
        # requested step is not used.
        abs_step = (
            rel_step * sign_x0 * np.abs(x0)
        ).astype(x0.dtype)

        # however we don't want an abs_step of 0, which can happen if
        # rel_step is 0, or x0 is 0. Instead, substitute a realistic step
        dx = ((x0 + abs_step) - x0)
        abs_step = np.where(
            dx == 0,
            default_abs_step,
            abs_step
        )

    return abs_step

