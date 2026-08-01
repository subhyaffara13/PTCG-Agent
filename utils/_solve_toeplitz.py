
def _solve_toeplitz(c, r, b, check_finite):
    r, c, b, dtype, b_shape = _validate_args_for_toeplitz_ops(
        (c, r), b, check_finite, keep_b_shape=True)

    # accommodate empty arrays
    if b.size == 0:
        return np.empty_like(b)

    # Form a 1-D array of values to be used in the matrix, containing a
    # reversed copy of r[1:], followed by c.
    vals = np.concatenate((r[-1:0:-1], c))
    if b is None:
        raise ValueError('illegal value, `b` is a required argument')

    if b.ndim == 1:
        x, _ = levinson(vals, np.ascontiguousarray(b))
    else:
        x = np.column_stack([levinson(vals, np.ascontiguousarray(b[:, i]))[0]
                             for i in range(b.shape[1])])
        x = x.reshape(*b_shape)

    return x

