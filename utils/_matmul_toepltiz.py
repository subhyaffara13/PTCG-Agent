
def _matmul_toepltiz(r, c, x, workers, check_finite, fft, ifft, rfft, irfft):
    r, c, x, dtype, x_shape = _validate_args_for_toeplitz_ops((c, r), x, check_finite,
                                                              keep_b_shape=False,
                                                              enforce_square=False)
    n, m = x.shape

    T_nrows = len(c)
    T_ncols = len(r)
    p = T_nrows + T_ncols - 1  # equivalent to len(embedded_col)
    return_shape = (T_nrows,) if len(x_shape) == 1 else (T_nrows, m)

    # accommodate empty arrays
    if x.size == 0:
        return np.empty_like(x, shape=return_shape)

    embedded_col = np.concatenate((c, r[-1:0:-1]))

    if np.iscomplexobj(embedded_col) or np.iscomplexobj(x):
        fft_mat = fft(embedded_col, axis=0, workers=workers).reshape(-1, 1)
        fft_x = fft(x, n=p, axis=0, workers=workers)

        mat_times_x = ifft(fft_mat*fft_x, axis=0,
                           workers=workers)[:T_nrows, :]
    else:
        # Real inputs; using rfft is faster
        fft_mat = rfft(embedded_col, axis=0, workers=workers).reshape(-1, 1)
        fft_x = rfft(x, n=p, axis=0, workers=workers)

        mat_times_x = irfft(fft_mat*fft_x, axis=0,
                            workers=workers, n=p)[:T_nrows, :]

    return mat_times_x.reshape(*return_shape)

