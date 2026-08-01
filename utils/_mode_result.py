
def _mode_result(mode, count):
    # When a slice is empty, `_axis_nan_policy` automatically produces
    # NaN for `mode` and `count`. This is a reasonable convention for `mode`,
    # but `count` should not be NaN; it should be zero.
    xp = array_namespace(mode, count)
    i = xp.isnan(count)
    if i.shape == ():
        count = xp.asarray(0, dtype=count.dtype)[()] if i else count
    else:
        count = xpx.at(count)[i].set(0)
    if is_numpy(xp) and mode.ndim > 0:
        # When a) xp is NumPy, b) array is multidimensional, c) NaNs are present,
        # and d) nan_policy='omit', `_axis_nan_policy` decorator uses
        # `np.apply_along_axis` to compute mode/count along each axis-slice separately.
        # The result is a single array with the result dtype of `mode` and `count`.
        # We need to change `count` back to an integer.
        count = xp.astype(count, xp.asarray(0).dtype)
    return ModeResult(mode, count)

