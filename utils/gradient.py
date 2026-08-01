
def gradient(f: ArrayLike, *varargs, axis=None, edge_order=1):
    N = f.ndim  # number of dimensions

    varargs = _util.ndarrays_to_tensors(varargs)

    if axis is None:
        axes = tuple(range(N))
    else:
        axes = _util.normalize_axis_tuple(axis, N)

    len_axes = len(axes)
    n = len(varargs)
    if n == 0:
        # no spacing argument - use 1 in all axes
        dx = [1.0] * len_axes
    elif n == 1 and (_dtypes_impl.is_scalar(varargs[0]) or varargs[0].ndim == 0):
        # single scalar or 0D tensor for all axes (np.ndim(varargs[0]) == 0)
        dx = varargs * len_axes
    elif n == len_axes:
        # scalar or 1d array for each axis
        dx = list(varargs)
        for i, distances in enumerate(dx):
            distances = torch.as_tensor(distances)
            if distances.ndim == 0:
                continue
            elif distances.ndim != 1:
                raise ValueError("distances must be either scalars or 1d")
            if len(distances) != f.shape[axes[i]]:
                raise ValueError(
                    "when 1d, distances must match "
                    "the length of the corresponding dimension"
                )
            if not (distances.dtype.is_floating_point or distances.dtype.is_complex):
                distances = distances.double()

            diffx = torch.diff(distances)
            # if distances are constant reduce to the scalar case
            # since it brings a consistent speedup
            if (diffx == diffx[0]).all():
                diffx = diffx[0]
            dx[i] = diffx
    else:
        raise TypeError("invalid number of arguments")

    if edge_order > 2:
        raise ValueError("'edge_order' greater than 2 not supported")

    # use central differences on interior and one-sided differences on the
    # endpoints. This preserves second order-accuracy over the full domain.

    outvals = []

    # create slice objects --- initially all are [:, :, ..., :]
    slice1 = [slice(None)] * N
    slice2 = [slice(None)] * N
    slice3 = [slice(None)] * N
    slice4 = [slice(None)] * N

    otype = f.dtype
    if _dtypes_impl.python_type_for_torch(otype) in (int, bool):
        # Convert to floating point.
        # First check if f is a numpy integer type; if so, convert f to float64
        # to avoid modular arithmetic when computing the changes in f.
        f = f.double()
        otype = torch.float64

    for axis, ax_dx in zip(axes, dx):
        if f.shape[axis] < edge_order + 1:
            raise ValueError(
                "Shape of array too small to calculate a numerical gradient, "
                "at least (edge_order + 1) elements are required."
            )
        # result allocation
        out = torch.empty_like(f, dtype=otype)

        # spacing for the current axis (NB: np.ndim(ax_dx) == 0)
        uniform_spacing = _dtypes_impl.is_scalar(ax_dx) or ax_dx.ndim == 0

        # Numerical differentiation: 2nd order interior
        slice1[axis] = slice(1, -1)
        slice2[axis] = slice(None, -2)
        slice3[axis] = slice(1, -1)
        slice4[axis] = slice(2, None)

        if uniform_spacing:
            out[tuple(slice1)] = (f[tuple(slice4)] - f[tuple(slice2)]) / (2.0 * ax_dx)
        else:
            dx1 = ax_dx[0:-1]
            dx2 = ax_dx[1:]
            a = -(dx2) / (dx1 * (dx1 + dx2))
            b = (dx2 - dx1) / (dx1 * dx2)
            c = dx1 / (dx2 * (dx1 + dx2))
            # fix the shape for broadcasting
            shape = [1] * N
            shape[axis] = -1
            a = a.reshape(shape)
            b = b.reshape(shape)
            c = c.reshape(shape)
            # 1D equivalent -- out[1:-1] = a * f[:-2] + b * f[1:-1] + c * f[2:]
            out[tuple(slice1)] = (
                a * f[tuple(slice2)] + b * f[tuple(slice3)] + c * f[tuple(slice4)]
            )

        # Numerical differentiation: 1st order edges
        if edge_order == 1:
            slice1[axis] = 0
            slice2[axis] = 1
            slice3[axis] = 0
            dx_0 = ax_dx if uniform_spacing else ax_dx[0]
            # 1D equivalent -- out[0] = (f[1] - f[0]) / (x[1] - x[0])
            out[tuple(slice1)] = (f[tuple(slice2)] - f[tuple(slice3)]) / dx_0

            slice1[axis] = -1
            slice2[axis] = -1
            slice3[axis] = -2
            dx_n = ax_dx if uniform_spacing else ax_dx[-1]
            # 1D equivalent -- out[-1] = (f[-1] - f[-2]) / (x[-1] - x[-2])
            out[tuple(slice1)] = (f[tuple(slice2)] - f[tuple(slice3)]) / dx_n

        # Numerical differentiation: 2nd order edges
        else:
            slice1[axis] = 0
            slice2[axis] = 0
            slice3[axis] = 1
            slice4[axis] = 2
            if uniform_spacing:
                a = -1.5 / ax_dx
                b = 2.0 / ax_dx
                c = -0.5 / ax_dx
            else:
                dx1 = ax_dx[0]
                dx2 = ax_dx[1]
                a = -(2.0 * dx1 + dx2) / (dx1 * (dx1 + dx2))
                b = (dx1 + dx2) / (dx1 * dx2)
                c = -dx1 / (dx2 * (dx1 + dx2))
            # 1D equivalent -- out[0] = a * f[0] + b * f[1] + c * f[2]
            out[tuple(slice1)] = (
                a * f[tuple(slice2)] + b * f[tuple(slice3)] + c * f[tuple(slice4)]
            )

            slice1[axis] = -1
            slice2[axis] = -3
            slice3[axis] = -2
            slice4[axis] = -1
            if uniform_spacing:
                a = 0.5 / ax_dx
                b = -2.0 / ax_dx
                c = 1.5 / ax_dx
            else:
                dx1 = ax_dx[-2]
                dx2 = ax_dx[-1]
                a = (dx2) / (dx1 * (dx1 + dx2))
                b = -(dx2 + dx1) / (dx1 * dx2)
                c = (2.0 * dx2 + dx1) / (dx2 * (dx1 + dx2))
            # 1D equivalent -- out[-1] = a * f[-3] + b * f[-2] + c * f[-1]
            out[tuple(slice1)] = (
                a * f[tuple(slice2)] + b * f[tuple(slice3)] + c * f[tuple(slice4)]
            )

        outvals.append(out)

        # reset the slice object in this dimension to ":"
        slice1[axis] = slice(None)
        slice2[axis] = slice(None)
        slice3[axis] = slice(None)
        slice4[axis] = slice(None)

    if len_axes == 1:
        return outvals[0]
    else:
        return outvals


def gradient(scalar_field, doit=True):
    """
    Returns the vector gradient of a scalar field computed wrt the
    base scalars of the given coordinate system.

    Parameters
    ==========

    scalar_field : SymPy Expr
        The scalar field to compute the gradient of

    doit : bool
        If True, the result is returned after calling .doit() on
        each component. Else, the returned expression contains
        Derivative instances

    Examples
    ========

    >>> from sympy.vector import CoordSys3D, gradient
    >>> R = CoordSys3D('R')
    >>> s1 = R.x*R.y*R.z
    >>> gradient(s1)
    R.y*R.z*R.i + R.x*R.z*R.j + R.x*R.y*R.k
    >>> s2 = 5*R.x**2*R.z
    >>> gradient(s2)
    10*R.x*R.z*R.i + 5*R.x**2*R.k

    """
    coord_sys = _get_coord_systems(scalar_field)

    if len(coord_sys) == 0:
        return Vector.zero
    elif len(coord_sys) == 1:
        coord_sys = next(iter(coord_sys))
        h1, h2, h3 = coord_sys.lame_coefficients()
        i, j, k = coord_sys.base_vectors()
        x, y, z = coord_sys.base_scalars()
        vx = Derivative(scalar_field, x) / h1
        vy = Derivative(scalar_field, y) / h2
        vz = Derivative(scalar_field, z) / h3

        if doit:
            return (vx * i + vy * j + vz * k).doit()
        return vx * i + vy * j + vz * k
    else:
        if isinstance(scalar_field, (Add, VectorAdd)):
            return VectorAdd.fromiter(gradient(i) for i in scalar_field.args)
        if isinstance(scalar_field, (Mul, VectorMul)):
            s = _split_mul_args_wrt_coordsys(scalar_field)
            return VectorAdd.fromiter(scalar_field / i * gradient(i) for i in s)
        return Gradient(scalar_field)


def gradient(scalar, frame):
    """
    Returns the vector gradient of a scalar field computed wrt the
    coordinate symbols of the given frame.

    Parameters
    ==========

    scalar : sympifiable
        The scalar field to take the gradient of

    frame : ReferenceFrame
        The frame to calculate the gradient in

    Examples
    ========

    >>> from sympy.physics.vector import ReferenceFrame
    >>> from sympy.physics.vector import gradient
    >>> R = ReferenceFrame('R')
    >>> s1 = R[0]*R[1]*R[2]
    >>> gradient(s1, R)
    R_y*R_z*R.x + R_x*R_z*R.y + R_x*R_y*R.z
    >>> s2 = 5*R[0]**2*R[2]
    >>> gradient(s2, R)
    10*R_x*R_z*R.x + 5*R_x**2*R.z

    """

    _check_frame(frame)
    outvec = Vector(0)
    scalar = express(scalar, frame, variables=True)
    for i, x in enumerate(frame):
        outvec += diff(scalar, frame[i]) * x  # noqa: PLR1736
    return outvec


def gradient(width, height):
    """

    Yields a pt and corresponding RGBA tuple, for every (width, height) combo.
    Useful for generating gradients.

    Actual gradient may be changed, no tests rely on specific values.

    Used in transform.rotate lossless tests to generate a fixture.

    """

    for l in range(width):
        for t in range(height):
            yield (l, t), tuple(map(rgba_between, (l, t, l, l + t)))


def gradient(f, *varargs, axis=None, edge_order=1):
    """
    Return the gradient of an N-dimensional array.

    The gradient is computed using second order accurate central differences
    in the interior points and either first or second order accurate one-sides
    (forward or backwards) differences at the boundaries.
    The returned gradient hence has the same shape as the input array.

    Parameters
    ----------
    f : array_like
        An N-dimensional array containing samples of a scalar function.
    varargs : list of scalar or array, optional
        Spacing between f values. Default unitary spacing for all dimensions.
        Spacing can be specified using:

        1. Single scalar to specify a sample distance for all dimensions.
        2. N scalars to specify a constant sample distance for each dimension.
           i.e. `dx`, `dy`, `dz`, ...
        3. N arrays to specify the coordinates of the values along each
           dimension of F. The length of the array must match the size of
           the corresponding dimension
        4. Any combination of N scalars/arrays with the meaning of 2. and 3.

        If `axis` is given, the number of varargs must equal the number of axes
        specified in the axis parameter.
        Default: 1. (see Examples below).

    edge_order : {1, 2}, optional
        Gradient is calculated using N-th order accurate differences
        at the boundaries. Default: 1.
    axis : None or int or tuple of ints, optional
        Gradient is calculated only along the given axis or axes.
        The default (axis = None) is to calculate the gradient for all the axes
        of the input array. axis may be negative, in which case it counts from
        the last to the first axis.

    Returns
    -------
    gradient : ndarray or tuple of ndarray
        A tuple of ndarrays (or a single ndarray if there is only one
        dimension) corresponding to the derivatives of f with respect
        to each dimension. Each derivative has the same shape as f.

    Examples
    --------
    >>> import numpy as np
    >>> f = np.array([1, 2, 4, 7, 11, 16])
    >>> np.gradient(f)
    array([1. , 1.5, 2.5, 3.5, 4.5, 5. ])
    >>> np.gradient(f, 2)
    array([0.5 ,  0.75,  1.25,  1.75,  2.25,  2.5 ])

    Spacing can be also specified with an array that represents the coordinates
    of the values F along the dimensions.
    For instance a uniform spacing:

    >>> x = np.arange(f.size)
    >>> np.gradient(f, x)
    array([1. ,  1.5,  2.5,  3.5,  4.5,  5. ])

    Or a non uniform one:

    >>> x = np.array([0., 1., 1.5, 3.5, 4., 6.])
    >>> np.gradient(f, x)
    array([1. ,  3. ,  3.5,  6.7,  6.9,  2.5])

    For two dimensional arrays, the return will be two arrays ordered by
    axis. In this example the first array stands for the gradient in
    rows and the second one in columns direction:

    >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]]))
    (array([[ 2.,  2., -1.],
            [ 2.,  2., -1.]]),
     array([[1. , 2.5, 4. ],
            [1. , 1. , 1. ]]))

    In this example the spacing is also specified:
    uniform for axis=0 and non uniform for axis=1

    >>> dx = 2.
    >>> y = [1., 1.5, 3.5]
    >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]]), dx, y)
    (array([[ 1. ,  1. , -0.5],
            [ 1. ,  1. , -0.5]]),
     array([[2. , 2. , 2. ],
            [2. , 1.7, 0.5]]))

    It is possible to specify how boundaries are treated using `edge_order`

    >>> x = np.array([0, 1, 2, 3, 4])
    >>> f = x**2
    >>> np.gradient(f, edge_order=1)
    array([1.,  2.,  4.,  6.,  7.])
    >>> np.gradient(f, edge_order=2)
    array([0., 2., 4., 6., 8.])

    The `axis` keyword can be used to specify a subset of axes of which the
    gradient is calculated

    >>> np.gradient(np.array([[1, 2, 6], [3, 4, 5]]), axis=0)
    array([[ 2.,  2., -1.],
           [ 2.,  2., -1.]])

    The `varargs` argument defines the spacing between sample points in the
    input array. It can take two forms:

    1. An array, specifying coordinates, which may be unevenly spaced:

    >>> x = np.array([0., 2., 3., 6., 8.])
    >>> y = x ** 2
    >>> np.gradient(y, x, edge_order=2)
    array([ 0.,  4.,  6., 12., 16.])

    2. A scalar, representing the fixed sample distance:

    >>> dx = 2
    >>> x = np.array([0., 2., 4., 6., 8.])
    >>> y = x ** 2
    >>> np.gradient(y, dx, edge_order=2)
    array([ 0.,  4.,  8., 12., 16.])

    It's possible to provide different data for spacing along each dimension.
    The number of arguments must match the number of dimensions in the input
    data.

    >>> dx = 2
    >>> dy = 3
    >>> x = np.arange(0, 6, dx)
    >>> y = np.arange(0, 9, dy)
    >>> xs, ys = np.meshgrid(x, y)
    >>> zs = xs + 2 * ys
    >>> np.gradient(zs, dy, dx)  # Passing two scalars
    (array([[2., 2., 2.],
            [2., 2., 2.],
            [2., 2., 2.]]),
     array([[1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.]]))

    Mixing scalars and arrays is also allowed:

    >>> np.gradient(zs, y, dx)  # Passing one array and one scalar
    (array([[2., 2., 2.],
            [2., 2., 2.],
            [2., 2., 2.]]),
     array([[1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.]]))

    Notes
    -----
    Assuming that :math:`f\\in C^{3}` (i.e., :math:`f` has at least 3 continuous
    derivatives) and let :math:`h_{*}` be a non-homogeneous stepsize, we
    minimize the "consistency error" :math:`\\eta_{i}` between the true gradient
    and its estimate from a linear combination of the neighboring grid-points:

    .. math::

        \\eta_{i} = f_{i}^{\\left(1\\right)} -
                    \\left[ \\alpha f\\left(x_{i}\\right) +
                            \\beta f\\left(x_{i} + h_{d}\\right) +
                            \\gamma f\\left(x_{i}-h_{s}\\right)
                    \\right]

    By substituting :math:`f(x_{i} + h_{d})` and :math:`f(x_{i} - h_{s})`
    with their Taylor series expansion, this translates into solving
    the following the linear system:

    .. math::

        \\left\\{
            \\begin{array}{r}
                \\alpha+\\beta+\\gamma=0 \\\\
                \\beta h_{d}-\\gamma h_{s}=1 \\\\
                \\beta h_{d}^{2}+\\gamma h_{s}^{2}=0
            \\end{array}
        \\right.

    The resulting approximation of :math:`f_{i}^{(1)}` is the following:

    .. math::

        \\hat f_{i}^{(1)} =
            \\frac{
                h_{s}^{2}f\\left(x_{i} + h_{d}\\right)
                + \\left(h_{d}^{2} - h_{s}^{2}\\right)f\\left(x_{i}\\right)
                - h_{d}^{2}f\\left(x_{i}-h_{s}\\right)}
                { h_{s}h_{d}\\left(h_{d} + h_{s}\\right)}
            + \\mathcal{O}\\left(\\frac{h_{d}h_{s}^{2}
                                + h_{s}h_{d}^{2}}{h_{d}
                                + h_{s}}\\right)

    It is worth noting that if :math:`h_{s}=h_{d}`
    (i.e., data are evenly spaced)
    we find the standard second order approximation:

    .. math::

        \\hat f_{i}^{(1)}=
            \\frac{f\\left(x_{i+1}\\right) - f\\left(x_{i-1}\\right)}{2h}
            + \\mathcal{O}\\left(h^{2}\\right)

    With a similar procedure the forward/backward approximations used for
    boundaries can be derived.

    References
    ----------
    .. [1]  Quarteroni A., Sacco R., Saleri F. (2007) Numerical Mathematics
            (Texts in Applied Mathematics). New York: Springer.
    .. [2]  Durran D. R. (1999) Numerical Methods for Wave Equations
            in Geophysical Fluid Dynamics. New York: Springer.
    .. [3]  Fornberg B. (1988) Generation of Finite Difference Formulas on
            Arbitrarily Spaced Grids,
            Mathematics of Computation 51, no. 184 : 699-706.
            `PDF <https://www.ams.org/journals/mcom/1988-51-184/
            S0025-5718-1988-0935077-0/S0025-5718-1988-0935077-0.pdf>`_.
    """
    f = np.asanyarray(f)
    N = f.ndim  # number of dimensions

    if axis is None:
        axes = tuple(range(N))
    else:
        axes = _nx.normalize_axis_tuple(axis, N)

    len_axes = len(axes)
    n = len(varargs)
    if n == 0:
        # no spacing argument - use 1 in all axes
        dx = [1.0] * len_axes
    elif n == 1 and np.ndim(varargs[0]) == 0:
        # single scalar for all axes
        dx = varargs * len_axes
    elif n == len_axes:
        # scalar or 1d array for each axis
        dx = list(varargs)
        for i, distances in enumerate(dx):
            distances = np.asanyarray(distances)
            if distances.ndim == 0:
                continue
            elif distances.ndim != 1:
                raise ValueError("distances must be either scalars or 1d")
            if len(distances) != f.shape[axes[i]]:
                raise ValueError("when 1d, distances must match "
                                 "the length of the corresponding dimension")
            if np.issubdtype(distances.dtype, np.integer):
                # Convert numpy integer types to float64 to avoid modular
                # arithmetic in np.diff(distances).
                distances = distances.astype(np.float64)
            diffx = np.diff(distances)
            # if distances are constant reduce to the scalar case
            # since it brings a consistent speedup
            if (diffx == diffx[0]).all():
                diffx = diffx[0]
            dx[i] = diffx
    else:
        raise TypeError("invalid number of arguments")

    if edge_order > 2:
        raise ValueError("'edge_order' greater than 2 not supported")

    # use central differences on interior and one-sided differences on the
    # endpoints. This preserves second order-accuracy over the full domain.

    outvals = []

    # create slice objects --- initially all are [:, :, ..., :]
    slice1 = [slice(None)] * N
    slice2 = [slice(None)] * N
    slice3 = [slice(None)] * N
    slice4 = [slice(None)] * N

    otype = f.dtype
    if otype.type is np.datetime64:
        # the timedelta dtype with the same unit information
        otype = np.dtype(otype.name.replace('datetime', 'timedelta'))
        # view as timedelta to allow addition
        f = f.view(otype)
    elif otype.type is np.timedelta64:
        pass
    elif np.issubdtype(otype, np.inexact):
        pass
    else:
        # All other types convert to floating point.
        # First check if f is a numpy integer type; if so, convert f to float64
        # to avoid modular arithmetic when computing the changes in f.
        if np.issubdtype(otype, np.integer):
            f = f.astype(np.float64)
        otype = np.float64

    for axis, ax_dx in zip(axes, dx):
        if f.shape[axis] < edge_order + 1:
            raise ValueError(
                "Shape of array too small to calculate a numerical gradient, "
                "at least (edge_order + 1) elements are required.")
        # result allocation
        out = np.empty_like(f, dtype=otype)

        # spacing for the current axis
        uniform_spacing = np.ndim(ax_dx) == 0

        # Numerical differentiation: 2nd order interior
        slice1[axis] = slice(1, -1)
        slice2[axis] = slice(None, -2)
        slice3[axis] = slice(1, -1)
        slice4[axis] = slice(2, None)

        if uniform_spacing:
            out[tuple(slice1)] = (f[tuple(slice4)] - f[tuple(slice2)]) / (2. * ax_dx)
        else:
            dx1 = ax_dx[0:-1]
            dx2 = ax_dx[1:]
            a = -(dx2) / (dx1 * (dx1 + dx2))
            b = (dx2 - dx1) / (dx1 * dx2)
            c = dx1 / (dx2 * (dx1 + dx2))
            # fix the shape for broadcasting
            shape = np.ones(N, dtype=int)
            shape[axis] = -1

            a = a.reshape(shape)
            b = b.reshape(shape)
            c = c.reshape(shape)
            # 1D equivalent -- out[1:-1] = a * f[:-2] + b * f[1:-1] + c * f[2:]
            out[tuple(slice1)] = a * f[tuple(slice2)] + b * f[tuple(slice3)] \
                                                + c * f[tuple(slice4)]

        # Numerical differentiation: 1st order edges
        if edge_order == 1:
            slice1[axis] = 0
            slice2[axis] = 1
            slice3[axis] = 0
            dx_0 = ax_dx if uniform_spacing else ax_dx[0]
            # 1D equivalent -- out[0] = (f[1] - f[0]) / (x[1] - x[0])
            out[tuple(slice1)] = (f[tuple(slice2)] - f[tuple(slice3)]) / dx_0

            slice1[axis] = -1
            slice2[axis] = -1
            slice3[axis] = -2
            dx_n = ax_dx if uniform_spacing else ax_dx[-1]
            # 1D equivalent -- out[-1] = (f[-1] - f[-2]) / (x[-1] - x[-2])
            out[tuple(slice1)] = (f[tuple(slice2)] - f[tuple(slice3)]) / dx_n

        # Numerical differentiation: 2nd order edges
        else:
            slice1[axis] = 0
            slice2[axis] = 0
            slice3[axis] = 1
            slice4[axis] = 2
            if uniform_spacing:
                a = -1.5 / ax_dx
                b = 2. / ax_dx
                c = -0.5 / ax_dx
            else:
                dx1 = ax_dx[0]
                dx2 = ax_dx[1]
                a = -(2. * dx1 + dx2) / (dx1 * (dx1 + dx2))
                b = (dx1 + dx2) / (dx1 * dx2)
                c = - dx1 / (dx2 * (dx1 + dx2))
            # 1D equivalent -- out[0] = a * f[0] + b * f[1] + c * f[2]
            out[tuple(slice1)] = a * f[tuple(slice2)] + b * f[tuple(slice3)] \
                                                        + c * f[tuple(slice4)]

            slice1[axis] = -1
            slice2[axis] = -3
            slice3[axis] = -2
            slice4[axis] = -1
            if uniform_spacing:
                a = 0.5 / ax_dx
                b = -2. / ax_dx
                c = 1.5 / ax_dx
            else:
                dx1 = ax_dx[-2]
                dx2 = ax_dx[-1]
                a = (dx2) / (dx1 * (dx1 + dx2))
                b = - (dx2 + dx1) / (dx1 * dx2)
                c = (2. * dx2 + dx1) / (dx2 * (dx1 + dx2))
            # 1D equivalent -- out[-1] = a * f[-3] + b * f[-2] + c * f[-1]
            out[tuple(slice1)] = a * f[tuple(slice2)] + b * f[tuple(slice3)] \
                                                        + c * f[tuple(slice4)]

        outvals.append(out)

        # reset the slice object in this dimension to ":"
        slice1[axis] = slice(None)
        slice2[axis] = slice(None)
        slice3[axis] = slice(None)
        slice4[axis] = slice(None)

    if len_axes == 1:
        return outvals[0]
    return tuple(outvals)


def gradient(
    f: ArrayLike,
    *varargs: ArrayLike,
    axis: int | Sequence[int] | None = None,
    edge_order: int | None = None,
) -> Array | list[Array]:
  """Compute the numerical gradient of a sampled function.

  JAX implementation of :func:`numpy.gradient`.

  The gradient in ``jnp.gradient`` is computed using second-order finite
  differences across the array of sampled function values. This should not
  be confused with :func:`jax.grad`, which computes a precise gradient of
  a callable function via :ref:`automatic differentiation <automatic-differentiation>`.

  Args:
    f: *N*-dimensional array of function values.
    varargs: optional list of scalars or arrays specifying spacing of
      function evaluations. Options are:

      - not specified: unit spacing in all dimensions.
      - a single scalar: constant spacing in all dimensions.
      - *N* values: specify different spacing in each dimension:

        - scalar values indicate constant spacing in that dimension.
        - array values must match the length of the corresponding dimension,
          and specify the coordinates at which ``f`` is evaluated.

    edge_order: not implemented in JAX
    axis: integer or tuple of integers specifying the axis along which
      to compute the gradient. If None (default) calculates the gradient
      along all axes.

  Returns:
    an array or tuple of arrays containing the numerical gradient along
    each specified axis.

  See also:
    - :func:`jax.grad`: automatic differentiation of a function with a single output.

  Examples:
    Comparing numerical and automatic differentiation of a simple function:

    >>> def f(x):
    ...   return jnp.sin(x) * jnp.exp(-x / 4)
    ...
    >>> def gradf_exact(x):
    ...   # exact analytical gradient of f(x)
    ...   return -f(x) / 4 + jnp.cos(x) * jnp.exp(-x / 4)
    ...
    >>> x = jnp.linspace(0, 5, 10)

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print("numerical gradient:", jnp.gradient(f(x), x))
    ...   print("automatic gradient:", jax.vmap(jax.grad(f))(x))
    ...   print("exact gradient:    ", gradf_exact(x))
    ...
    numerical gradient: [ 0.83  0.61  0.18 -0.2  -0.43 -0.49 -0.39 -0.21 -0.02  0.08]
    automatic gradient: [ 1.    0.62  0.17 -0.23 -0.46 -0.51 -0.41 -0.21 -0.01  0.15]
    exact gradient:     [ 1.    0.62  0.17 -0.23 -0.46 -0.51 -0.41 -0.21 -0.01  0.15]

    Notice that, as expected, the numerical gradient has some approximation error
    compared to the automatic gradient computed via :func:`jax.grad`.
  """

  if edge_order is not None:
    raise NotImplementedError(
        "The 'edge_order' argument to jnp.gradient is not supported."
    )
  a, *spacing = util.promote_dtypes_inexact(f, *varargs)

  def gradient_along_axis(a, h, axis):
    sliced = partial(lax_slicing.slice_in_dim, a, axis=axis)
    upper_edge = sliced(1, 2) - sliced(0, 1)
    lower_edge = sliced(-1, None) - sliced(-2, -1)

    if np.ndim(h) == 0:
      inner = (sliced(2, None) - sliced(None, -2)) * 0.5 / h
      lower_edge /= h
      upper_edge /= h

    elif np.ndim(h) == 1:
      if len(h) != a.shape[axis]:
        raise ValueError(
            "Spacing arrays must have the same length as the "
            "dimension along which the gradient is calculated."
        )
      h_shape = [1] * a.ndim
      h_shape[axis] = len(h)
      h = h.reshape(h_shape)
      sliced_x = partial(lax_slicing.slice_in_dim, h, axis=axis)

      upper_edge /= sliced_x(1, 2) - sliced_x(0, 1)
      lower_edge /= sliced_x(-1, None) - sliced_x(-2, -1)
      dx1 = sliced_x(1, -1) - sliced_x(0, -2)
      dx2 = sliced_x(2, None) - sliced_x(1, -1)
      a = -(dx2) / (dx1 * (dx1 + dx2))
      b = (dx2 - dx1) / (dx1 * dx2)
      c = dx1 / (dx2 * (dx1 + dx2))
      inner = a * sliced(0, -2) + b * sliced(1, -1) + c * sliced(2, None)
    else:
      raise ValueError("Spacing arrays must be 1D arrays or scalars.")

    return concatenate((upper_edge, inner, lower_edge), axis=axis)

  if axis is None:
    axis_tuple = tuple(range(a.ndim))
  else:
    axis_tuple = tuple(_canonicalize_axis(i, a.ndim) for i in _ensure_index_tuple(axis))
  if len(axis_tuple) == 0:
    return []

  if min(s for i, s in enumerate(a.shape) if i in axis_tuple) < 2:
    raise ValueError("Shape of array too small to calculate "
                     "a numerical gradient, "
                     "at least 2 elements are required.")
  if len(spacing) == 0:
    dx: Sequence[ArrayLike] = [1.0] * len(axis_tuple)
  elif len(spacing) == 1:
    dx = list(spacing) * len(axis_tuple)
  elif len(spacing) == len(axis_tuple):
    dx = list(spacing)
  else:
    raise TypeError(f"Invalid number of spacing arguments {len(spacing)} for {axis=}")

  a_grad = [gradient_along_axis(a, h, ax) for ax, h in zip(axis_tuple, dx)]
  return a_grad[0] if len(axis_tuple) == 1 else a_grad

