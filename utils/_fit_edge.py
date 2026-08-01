
def _fit_edge(x, window_start, window_stop, interp_start, interp_stop,
              axis, polyorder, deriv, delta, y):
    """
    Given an N-d array `x` and the specification of a slice of `x` from
    `window_start` to `window_stop` along `axis`, create an interpolating
    polynomial of each 1-D slice, and evaluate that polynomial in the slice
    from `interp_start` to `interp_stop`. Put the result into the
    corresponding slice of `y`.
    """
    xp = array_namespace(x)

    # Get the edge into a (window_length, -1) array.
    x_edge = axis_slice(x, start=window_start, stop=window_stop, axis=axis)
    if axis == 0 or axis == -x.ndim:
        xx_edge = x_edge
        swapped = False
    else:
        xx_edge = xp_swapaxes(x_edge, axis, 0, xp)
        swapped = True
    xx_edge = xp.reshape(xx_edge, (xx_edge.shape[0], -1))

    # Fit the edges.  poly_coeffs has shape (polyorder + 1, -1),
    # where '-1' is the same as in xx_edge.
    poly_coeffs = _pu.polyfit(
        xp.arange(
            0, window_stop - window_start, dtype=x.dtype, device=xp_device(x)
        ), xx_edge, polyorder, xp=xp
    )

    if deriv > 0:
        poly_coeffs = _polyder(poly_coeffs, deriv, xp=xp)

    # Compute the interpolated values for the edge.
    i = xp.arange(
        interp_start - window_start, interp_stop - window_start,
        dtype=poly_coeffs.dtype, device=xp_device(poly_coeffs)
    )
    values = _pu.polyval(poly_coeffs, xp.reshape(i, (-1, 1)), xp=xp) / (delta ** deriv)

    # Now put the values into the appropriate slice of y.
    # First reshape values to match y.
    shp = list(y.shape)
    shp[0], shp[axis] = shp[axis], shp[0]
    values = xp.reshape(values, (interp_stop - interp_start, *shp[1:]))
    if swapped:
        values = xp_swapaxes(values, 0, axis, xp)
    # Get a view of the data to be replaced by values.
    y_slice = [slice(None)] * y.ndim
    y_slice[axis] = slice(interp_start, interp_stop)
    y = xpx.at(y, tuple(y_slice)).set(values)

    return y

