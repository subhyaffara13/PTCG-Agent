
def _cho_solve_banded(cb, b, lower, overwrite_b, check_finite):
    if check_finite:
        cb = asarray_chkfinite(cb)
        b = asarray_chkfinite(b)
    else:
        cb = asarray(cb)
        b = asarray(b)

    # Validate shapes.
    if cb.shape[-1] != b.shape[0]:
        raise ValueError("shapes of cb and b are not compatible.")

    # accommodate empty arrays
    if b.size == 0:
        m = cholesky_banded(np.array([[0, 0], [1, 1]], dtype=cb.dtype))
        dt = cho_solve_banded((m, True), np.ones(2, dtype=b.dtype)).dtype
        return empty_like(b, dtype=dt)

    pbtrs, = get_lapack_funcs(('pbtrs',), (cb, b))
    x, info = pbtrs(cb, b, lower=lower, overwrite_b=overwrite_b)
    if info > 0:
        raise LinAlgError(f"{info}th leading minor not positive definite")
    if info < 0:
        raise ValueError(f'illegal value in {-info}th argument of internal pbtrs')
    return x

