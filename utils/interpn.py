
def interpn(points, values, xi, method="linear", bounds_error=True,
            fill_value=np.nan):
    """
    Multidimensional interpolation on regular or rectilinear grids.

    Strictly speaking, not all regular grids are supported - this function
    works on *rectilinear* grids, that is, a rectangular grid with even or
    uneven spacing.

    Parameters
    ----------
    points : tuple of ndarray of float, with shapes (m1, ), ..., (mn, )
        The points defining the regular grid in n dimensions. The points in
        each dimension (i.e. every elements of the points tuple) must be
        strictly ascending or descending.

    values : array_like, shape (m1, ..., mn, ...)
        The data on the regular grid in n dimensions. Complex data is
        accepted.
    xi : ndarray of shape (..., ndim)
        The coordinates to sample the gridded data at

    method : str, optional
        The method of interpolation to perform. Supported are "linear",
        "nearest", "slinear", "cubic", "quintic", "pchip", and "splinef2d".
        "splinef2d" is only supported for 2-dimensional data.

    bounds_error : bool, optional
        If True, when interpolated values are requested outside of the
        domain of the input data, a ValueError is raised.
        If False, then `fill_value` is used.

    fill_value : number, optional
        If provided, the value to use for points outside of the
        interpolation domain. If None, values outside
        the domain are extrapolated.  Extrapolation is not supported by method
        "splinef2d".

    Returns
    -------
    values_x : ndarray, shape xi.shape[:-1] + values.shape[ndim:]
        Interpolated values at `xi`. See notes for behaviour when
        ``xi.ndim == 1``.

    See Also
    --------
    NearestNDInterpolator : Nearest neighbor interpolation on unstructured
                            data in N dimensions
    LinearNDInterpolator : Piecewise linear interpolant on unstructured data
                           in N dimensions
    RegularGridInterpolator : interpolation on a regular or rectilinear grid
                              in arbitrary dimensions (`interpn` wraps this
                              class).
    RectBivariateSpline : Bivariate spline approximation over a rectangular mesh
    scipy.ndimage.map_coordinates : interpolation on grids with equal spacing
                                    (suitable for e.g., N-D image resampling)

    Notes
    -----

    .. versionadded:: 0.14

    In the case that ``xi.ndim == 1`` a new axis is inserted into
    the 0 position of the returned array, values_x, so its shape is
    instead ``(1,) + values.shape[ndim:]``.

    If the input data is such that input dimensions have incommensurate
    units and differ by many orders of magnitude, the interpolant may have
    numerical artifacts. Consider rescaling the data before interpolation.

    Examples
    --------
    Evaluate a simple example function on the points of a regular 3-D grid:

    >>> import numpy as np
    >>> from scipy.interpolate import interpn
    >>> def value_func_3d(x, y, z):
    ...     return 2 * x + 3 * y - z
    >>> x = np.linspace(0, 4, 5)
    >>> y = np.linspace(0, 5, 6)
    >>> z = np.linspace(0, 6, 7)
    >>> points = (x, y, z)
    >>> values = value_func_3d(*np.meshgrid(*points, indexing='ij'))

    Evaluate the interpolating function at a point

    >>> point = np.array([2.21, 3.12, 1.15])
    >>> print(interpn(points, values, point))
    [12.63]

    Compare with value at point by function

    >>> value_func_3d(*point)
    12.63 # up to rounding

    Since the function is linear, the interpolation is exact using linear method.

    If ``fill_value=None``, then values outside of the domain are extrapolated.

    >>> x = np.linspace(0, 10, 11)
    >>> y = np.linspace(0, 15, 16)
    >>> def value_func_2d(x, y):
    ...    return 5 * x - 3 * y
    >>> points = (x, y)
    >>> values = value_func_2d(*np.meshgrid(*points, indexing='ij'))
    >>> xi = np.array([[25, 36]])
    >>> interpn(points, values, xi, method='linear', bounds_error=False,
    ...         fill_value=None)
    array([17.])

    If a ``fill_value`` is specified, any points outside the domain will be set to
    ``fill_value``.

    >>> interpn(points, values, xi, method='linear', bounds_error=False, fill_value=42)
    array([42.])

    When one axis is a single grid point, interpolation is only done at that
    coordinate. Any other value along that axis is out of bounds, and set
    to ``fill_value`` (if there is one).

    Evaluate interpolation function at a point outside of the single-point axis

    >>> x = np.array([0.0]) # x axis has length 1
    >>> y = np.linspace(0, 10, 11)
    >>> points = (x, y) 
    >>> values = value_func_2d(*np.meshgrid(*points, indexing='ij'))
    >>> xi = np.array([[1.0, 0.5]])
    >>> interpn(points, values, xi, method='linear', bounds_error=False,
    ...         fill_value = 42)
    array([42.])

    Evaluate interpolation function at a point on the single-point axis

    >>> xi = np.array([[0.0, 0.5]])
    >>> interpn(points, values, xi, method='linear', bounds_error=False,
    ...         fill_value = 42) 
    array([-1.5])   # interpolation as normal along y

    """
    # sanity check 'method' kwarg
    if method not in ["linear", "nearest", "cubic", "quintic", "pchip",
                      "splinef2d", "slinear",
                      "slinear_legacy", "cubic_legacy", "quintic_legacy"]:
        raise ValueError("interpn only understands the methods 'linear', "
                         "'nearest', 'slinear', 'cubic', 'quintic', 'pchip', "
                         f"and 'splinef2d'. You provided {method}.")

    if not hasattr(values, 'ndim'):
        values = np.asarray(values)

    ndim = values.ndim
    if ndim > 2 and method == "splinef2d":
        raise ValueError("The method splinef2d can only be used for "
                         "2-dimensional input data")
    if not bounds_error and fill_value is None and method == "splinef2d":
        raise ValueError("The method splinef2d does not support extrapolation.")

    # sanity check consistency of input dimensions
    if len(points) > ndim:
        raise ValueError(
            f"There are {len(points)} point arrays, but values has {ndim} dimensions"
        )
    if len(points) != ndim and method == 'splinef2d':
        raise ValueError("The method splinef2d can only be used for "
                         "scalar data with one point per coordinate")

    grid, descending_dimensions = _check_points(points)
    _check_dimensionality(grid, values)

    # sanity check requested xi
    xi = _ndim_coords_from_arrays(xi, ndim=len(grid))
    if xi.shape[-1] != len(grid):
        raise ValueError(
            f"The requested sample points xi have dimension {xi.shape[-1]}, "
            f"but this RegularGridInterpolator has dimension {len(grid)}"
        )

    if bounds_error:
        for i, p in enumerate(xi.T):
            if not np.logical_and(np.all(grid[i][0] <= p),
                                  np.all(p <= grid[i][-1])):
                raise ValueError(
                    f"One of the requested xi is out of bounds in dimension {i}"
                )

    # perform interpolation
    if method in RegularGridInterpolator._ALL_METHODS:
        interp = RegularGridInterpolator(points, values, method=method,
                                         bounds_error=bounds_error,
                                         fill_value=fill_value)
        return interp(xi)
    elif method == "splinef2d":
        xi_shape = xi.shape
        xi = xi.reshape(-1, xi.shape[-1])

        # RectBivariateSpline doesn't support fill_value; we need to wrap here
        idx_valid = np.all((grid[0][0] <= xi[:, 0], xi[:, 0] <= grid[0][-1],
                            grid[1][0] <= xi[:, 1], xi[:, 1] <= grid[1][-1]),
                           axis=0)
        result = np.empty_like(xi[:, 0])

        # make a copy of values for RectBivariateSpline
        interp = RectBivariateSpline(points[0], points[1], values[:])
        result[idx_valid] = interp.ev(xi[idx_valid, 0], xi[idx_valid, 1])
        result[np.logical_not(idx_valid)] = fill_value

        return result.reshape(xi_shape[:-1])
    else:
        raise ValueError(f"unknown {method = }")

