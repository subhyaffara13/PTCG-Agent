
def make_interp_spline(x, y, k=3, t=None, bc_type=None, axis=0,
                       check_finite=True):
    """Create an interpolating B-spline with specified degree and boundary conditions.

    Parameters
    ----------
    x : array_like, shape (n,)
        Abscissas.
    y : array_like, shape (n, ...)
        Ordinates.
    k : int, optional
        B-spline degree. Default is cubic, ``k = 3``.
    t : array_like, shape (nt + k + 1,), optional
        Knots.
        The number of knots needs to agree with the number of data points and
        the number of derivatives at the edges. Specifically, ``nt - n`` must
        equal ``len(deriv_l) + len(deriv_r)``.
    bc_type : 2-tuple or None
        Boundary conditions.
        Default is None, which means choosing the boundary conditions
        automatically. Otherwise, it must be a length-two tuple where the first
        element (``deriv_l``) sets the boundary conditions at ``x[0]`` and
        the second element (``deriv_r``) sets the boundary conditions at
        ``x[-1]``. Each of these must be an iterable of pairs
        ``(order, value)`` which gives the values of derivatives of specified
        orders at the given edge of the interpolation interval.
        Alternatively, the following string aliases are recognized:

        * ``"clamped"``: The first derivatives at the ends are zero. This is
          equivalent to ``bc_type=([(1, 0.0)], [(1, 0.0)])``.
        * ``"natural"``: The second derivatives at ends are zero. This is
          equivalent to ``bc_type=([(2, 0.0)], [(2, 0.0)])``.
        * ``"not-a-knot"`` (default): The first and second segments are the
          same polynomial. This is equivalent to having ``bc_type=None``.
        * ``"periodic"``: The values and the first ``k-1`` derivatives at the
          ends are equivalent.

    axis : int, optional
        Interpolation axis. Default is 0.
    check_finite : bool, optional
        Whether to check that the input arrays contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
        Default is True.

    Returns
    -------
    b : `BSpline` object
        A `BSpline` object of the degree ``k`` and with knots ``t``.

    See Also
    --------
    BSpline : base class representing the B-spline objects
    CubicSpline : a cubic spline in the polynomial basis
    make_lsq_spline : a similar factory function for spline fitting
    UnivariateSpline : a wrapper over FITPACK spline fitting routines
    splrep : a wrapper over FITPACK spline fitting routines

    Examples
    --------
    Use cubic interpolation on Chebyshev nodes:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> def cheb_nodes(N):
    ...     jj = 2.*np.arange(N) + 1
    ...     x = np.cos(np.pi * jj / 2 / N)[::-1]
    ...     return x

    >>> x = cheb_nodes(20)
    >>> y = np.sqrt(1 - x**2)

    >>> from scipy.interpolate import BSpline, make_interp_spline
    >>> b = make_interp_spline(x, y)
    >>> np.allclose(b(x), y)
    True

    Note that the default is a cubic spline with a not-a-knot boundary condition

    >>> b.k
    3

    Here we use a 'natural' spline, with zero 2nd derivatives at edges:

    >>> l, r = [(2, 0.0)], [(2, 0.0)]
    >>> b_n = make_interp_spline(x, y, bc_type=(l, r))  # or, bc_type="natural"
    >>> np.allclose(b_n(x), y)
    True
    >>> x0, x1 = x[0], x[-1]
    >>> np.allclose([b_n(x0, 2), b_n(x1, 2)], [0, 0])
    True

    Interpolation of parametric curves is also supported. As an example, we
    compute a discretization of a snail curve in polar coordinates

    >>> phi = np.linspace(0, 2.*np.pi, 40)
    >>> r = 0.3 + np.cos(phi)
    >>> x, y = r*np.cos(phi), r*np.sin(phi)  # convert to Cartesian coordinates

    Build an interpolating curve, parameterizing it by the angle

    >>> spl = make_interp_spline(phi, np.c_[x, y])

    Evaluate the interpolant on a finer grid (note that we transpose the result
    to unpack it into a pair of x- and y-arrays)

    >>> phi_new = np.linspace(0, 2.*np.pi, 100)
    >>> x_new, y_new = spl(phi_new).T

    Plot the result

    >>> plt.plot(x, y, 'o')
    >>> plt.plot(x_new, y_new, '-')
    >>> plt.show()

    Build a B-spline curve with 2 dimensional y

    >>> x = np.linspace(0, 2*np.pi, 10)
    >>> y = np.array([np.sin(x), np.cos(x)])

    Periodic condition is satisfied because y coordinates of points on the ends
    are equivalent

    >>> ax = plt.axes(projection='3d')
    >>> xx = np.linspace(0, 2*np.pi, 100)
    >>> bspl = make_interp_spline(x, y, k=5, bc_type='periodic', axis=1)
    >>> ax.plot3D(xx, *bspl(xx))
    >>> ax.scatter3D(x, *y, color='red')
    >>> plt.show()

    """
    # convert string aliases for the boundary conditions
    if bc_type is None or bc_type == 'not-a-knot' or bc_type == 'periodic':
        deriv_l, deriv_r = None, None
    elif isinstance(bc_type, str):
        deriv_l, deriv_r = bc_type, bc_type
    else:
        try:
            deriv_l, deriv_r = bc_type
        except TypeError as e:
            raise ValueError(f"Unknown boundary condition: {bc_type}") from e

    xp = array_namespace(x, y, t)
    x = _as_float_array(x, check_finite)
    y = _as_float_array(y, check_finite)

    axis = normalize_axis_index(axis, y.ndim)
    y = np.moveaxis(y, axis, 0)    # now internally interp axis is zero

    # sanity check the input
    if bc_type == 'periodic' and not np.allclose(y[0], y[-1], atol=1e-15):
        raise ValueError("First and last points does not match while "
                         "periodic case expected")
    if x.size != y.shape[0]:
        raise ValueError(f'Shapes of x {x.shape} and y {y.shape} are incompatible')
    if np.any(x[1:] == x[:-1]):
        raise ValueError("Expect x to not have duplicates")
    if x.ndim != 1 or np.any(x[1:] < x[:-1]):
        raise ValueError("Expect x to be a 1D strictly increasing sequence.")

    # special-case k=0 right away
    if k == 0:
        if any(_ is not None for _ in (t, deriv_l, deriv_r)):
            raise ValueError("Too much info for k=0: t and bc_type can only "
                             "be None.")
        t = np.r_[x, x[-1]]
        c = np.asarray(y)
        c = np.ascontiguousarray(c, dtype=_get_dtype(c.dtype))
        t, c = xp.asarray(t), xp.asarray(c)
        return BSpline.construct_fast(t, c, k, axis=axis)

    # special-case k=1 (e.g., Lyche and Morken, Eq.(2.16))
    if k == 1 and t is None:
        if not (deriv_l is None and deriv_r is None):
            raise ValueError("Too much info for k=1: bc_type can only be None.")
        t = np.r_[x[0], x, x[-1]]
        c = np.asarray(y)
        c = np.ascontiguousarray(c, dtype=_get_dtype(c.dtype))
        t, c = xp.asarray(t), xp.asarray(c)
        return BSpline.construct_fast(t, c, k, axis=axis)

    k = operator.index(k)

    if bc_type == 'periodic' and t is not None:
        raise NotImplementedError("For periodic case t is constructed "
                                  "automatically and can not be passed "
                                  "manually")

    # come up with a sensible knot vector, if needed
    if t is None:
        if deriv_l is None and deriv_r is None:
            if bc_type == 'periodic':
                t = _periodic_knots(x, k)
            else:
                t = _not_a_knot(x, k)
        else:
            t = _augknt(x, k)

    t = _as_float_array(t, check_finite)

    if k < 0:
        raise ValueError("Expect non-negative k.")
    if t.ndim != 1 or np.any(t[1:] < t[:-1]):
        raise ValueError("Expect t to be a 1-D sorted array_like.")
    if t.size < x.size + k + 1:
        raise ValueError(f"Got {t.size} knots, need at least {x.size + k + 1}.")
    if (x[0] < t[k]) or (x[-1] > t[-k]):
        raise ValueError(f'Out of bounds w/ x = {x}.')

    if bc_type == 'periodic':
        return _make_periodic_spline(x, y, t, k, axis, xp=xp)

    # Here : deriv_l, r = [(nu, value), ...]
    deriv_l = _convert_string_aliases(deriv_l, y.shape[1:])
    deriv_l_ords, deriv_l_vals = _process_deriv_spec(deriv_l)
    nleft = deriv_l_ords.shape[0]

    deriv_r = _convert_string_aliases(deriv_r, y.shape[1:])
    deriv_r_ords, deriv_r_vals = _process_deriv_spec(deriv_r)
    nright = deriv_r_ords.shape[0]

    if not all(0 <= i <= k for i in deriv_l_ords):
        raise ValueError(f"Bad boundary conditions at {x[0]}.")

    if not all(0 <= i <= k for i in deriv_r_ords):
        raise ValueError(f"Bad boundary conditions at {x[-1]}.")

    # have `n` conditions for `nt` coefficients; need nt-n derivatives
    n = x.size
    nt = t.size - k - 1

    if nt - n != nleft + nright:
        raise ValueError("The number of derivatives at boundaries does not "
                         f"match: expected {nt-n}, got {nleft}+{nright}")

    # bail out if the `y` array is zero-sized
    if y.size == 0:
        c = np.zeros((nt,) + y.shape[1:], dtype=float)
        return BSpline.construct_fast(t, c, k, axis=axis)

    # set up the LHS: the colocation matrix + derivatives at boundaries
    # NB: ab is in F order for banded LAPACK; _coloc needs C-ordered arrays,
    #     this pass ab.T into _coloc
    kl = ku = k
    ab = np.zeros((2*kl + ku + 1, nt), dtype=np.float64, order='F')
    _dierckx._coloc(x, t, k, ab.T, nleft)
    if nleft > 0:
        _handle_lhs_derivatives(t, k, x[0], ab, kl, ku, deriv_l_ords)
    if nright > 0:
        _handle_lhs_derivatives(t, k, x[-1], ab, kl, ku, deriv_r_ords,
                                offset=nt-nright)

    # set up the RHS: values to interpolate (+ derivative values, if any)
    extradim = prod(y.shape[1:])
    rhs = np.empty((nt, extradim), dtype=y.dtype)
    if nleft > 0:
        rhs[:nleft] = deriv_l_vals.reshape(-1, extradim)
    rhs[nleft:nt - nright] = y.reshape(-1, extradim)
    if nright > 0:
        rhs[nt - nright:] = deriv_r_vals.reshape(-1, extradim)

    # solve Ab @ x = rhs; this is the relevant part of linalg.solve_banded
    if check_finite:
        ab, rhs = map(np.asarray_chkfinite, (ab, rhs))
    gbsv, = get_lapack_funcs(('gbsv',), (ab, rhs))
    lu, piv, c, info = gbsv(kl, ku, ab, rhs,
                            overwrite_ab=True, overwrite_b=True)

    if info > 0:
        raise LinAlgError("Colocation matrix is singular.")
    elif info < 0:
        raise ValueError(f'illegal value in {-info}-th argument of internal gbsv')
    c = np.ascontiguousarray(c.reshape((nt,) + y.shape[1:]))
    t, c = xp.asarray(t), xp.asarray(c)
    return BSpline.construct_fast(t, c, k, axis=axis)

