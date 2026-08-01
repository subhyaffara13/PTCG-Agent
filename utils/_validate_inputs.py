
def _validate_inputs(x, y, w, k, s, xb, xe, parametric, periodic=False):
    """Common input validations for generate_knots and make_splrep.
    """
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    if not x.flags.c_contiguous:
        x = x.copy()
    if not y.flags.c_contiguous:
        y = y.copy()

    if w is None:
        w = np.ones_like(x, dtype=float)
    else:
        w = np.asarray(w, dtype=float)
        if not w.flags.c_contiguous:
            w = w.copy()
        if w.ndim != 1:
            raise ValueError(f"{w.ndim = } not implemented yet.")
        if (w < 0).any():
            raise ValueError("Weights must be non-negative")
        if w.sum() == 0:
            raise ValueError("All weights are zero.")


    if y.ndim == 0 or y.ndim > 2:
        raise ValueError(f"{y.ndim = } not supported (must be 1 or 2.)")

    parametric = bool(parametric)
    if parametric:
        if y.ndim != 2:
            raise ValueError(f"{y.ndim = } != 2 not supported with {parametric =}.")
    else:
        if y.ndim != 1:
            raise ValueError(f"{y.ndim = } != 1 not supported with {parametric =}.")
        # all _impl functions expect y.ndim = 2
        y = y[:, None]

    if w.shape[0] != x.shape[0]:
        raise ValueError(f"Weights is incompatible: {w.shape =} != {x.shape}.")

    if x.shape[0] != y.shape[0]:
        raise ValueError(f"Data is incompatible: {x.shape = } and {y.shape = }.")
    if x.ndim != 1 or (x[1:] < x[:-1]).any():
        raise ValueError("Expect `x` to be an ordered 1D sequence.")

    k = operator.index(k)

    if s < 0:
        raise ValueError(f"`s` must be non-negative. Got {s = }")

    if xb is None:
        xb = min(x)
    if xe is None:
        xe = max(x)

    if periodic and not np.allclose(y[0], y[-1], atol=1e-15):
        raise ValueError("First and last points does not match which is required "
                         "for `bc_type='periodic'`.")

    return x, y, w, k, s, xb, xe

