
def _execute_nD(func_str, duccfft_func, x, s, axes, norm, overwrite_x, workers, plan):
    xp = array_namespace(x)

    if is_numpy(xp):
        x = np.asarray(x)
        return duccfft_func(x, s=s, axes=axes, norm=norm,
                              overwrite_x=overwrite_x, workers=workers, plan=plan)

    norm = _validate_fft_args(workers, plan, norm)
    if hasattr(xp, 'fft'):
        xp_func = getattr(xp.fft, func_str)
        if func_str in complex_funcs:
            try:
                res = xp_func(x, s=s, axes=axes, norm=norm)
            except: # backends may require complex input  # noqa: E722
                x = xp_float_to_complex(x, xp)
                res = xp_func(x, s=s, axes=axes, norm=norm)
            return res
        return xp_func(x, s=s, axes=axes, norm=norm)

    x = np.asarray(x)
    y = duccfft_func(x, s=s, axes=axes, norm=norm)
    return xp.asarray(y)

