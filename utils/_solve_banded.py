
def _solve_banded(nlower, nupper, ab, b, overwrite_ab, overwrite_b, check_finite):
    a1 = _asarray_validated(ab, check_finite=check_finite, as_inexact=True)
    b1 = _asarray_validated(b, check_finite=check_finite, as_inexact=True)

    # Validate shapes.
    if a1.shape[-1] != b1.shape[0]:
        raise ValueError("shapes of ab and b are not compatible.")

    if nlower + nupper + 1 != a1.shape[0]:
        raise ValueError(
            f"invalid values for the number of lower and upper diagonals: l+u+1 "
            f"({nlower + nupper + 1}) does not equal ab.shape[0] ({ab.shape[0]})"
        )

    # accommodate empty arrays
    if b1.size == 0:
        dt = solve(np.eye(1, dtype=a1.dtype), np.ones(1, dtype=b1.dtype)).dtype
        return np.empty_like(b1, dtype=dt)

    overwrite_b = overwrite_b or _datacopied(b1, b)
    if a1.shape[-1] == 1:
        b2 = np.array(b1, copy=(not overwrite_b))
        # a1.shape[-1] == 1 -> original matrix is 1x1. Typically, the user
        # will pass u = l = 0 and `a1` will be 1x1. However, the rest of the
        # function works with unnecessary rows in `a1` as long as
        # `a1[u + i - j, j] == a[i,j]`. In the 1x1 case, we want i = j = 0,
        # so the diagonal is in row `u` of `a1`. See gh-8906.
        b2 /= a1[nupper, 0]
        return b2
    if nlower == nupper == 1:
        overwrite_ab = overwrite_ab or _datacopied(a1, ab)
        gtsv, = get_lapack_funcs(('gtsv',), (a1, b1))
        du = a1[0, 1:]
        d = a1[1, :]
        dl = a1[2, :-1]
        du2, d, du, x, info = gtsv(dl, d, du, b1, overwrite_ab, overwrite_ab,
                                   overwrite_ab, overwrite_b)
    else:
        gbsv, = get_lapack_funcs(('gbsv',), (a1, b1))
        a2 = np.zeros((2*nlower + nupper + 1, a1.shape[1]), dtype=gbsv.dtype)
        a2[nlower:, :] = a1
        lu, piv, x, info = gbsv(nlower, nupper, a2, b1, overwrite_ab=True,
                                overwrite_b=overwrite_b)
    if info == 0:
        return x
    if info > 0:
        raise LinAlgError("singular matrix")
    raise ValueError(f'illegal value in {-info}-th argument of internal gbsv/gtsv')

