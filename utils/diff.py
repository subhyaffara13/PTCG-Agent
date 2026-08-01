
def diff(*seqs, **kwargs):
    """ Return those items that differ between sequences

    >>> list(diff([1, 2, 3], [1, 2, 10, 100]))
    [(3, 10)]

    Shorter sequences may be padded with a ``default`` value:

    >>> list(diff([1, 2, 3], [1, 2, 10, 100], default=None))
    [(3, 10), (None, 100)]

    A ``key`` function may also be applied to each item to use during
    comparisons:

    >>> list(diff(['apples', 'bananas'], ['Apples', 'Oranges'], key=str.lower))
    [('bananas', 'Oranges')]
    """
    N = len(seqs)
    if N == 1 and isinstance(seqs[0], list):
        seqs = seqs[0]
        N = len(seqs)
    if N < 2:
        raise TypeError('Too few sequences given (min 2 required)')
    default = kwargs.get('default', no_default)
    if default == no_default:
        iters = zip(*seqs)
    else:
        iters = zip_longest(*seqs, fillvalue=default)
    key = kwargs.get('key', None)
    if key is None:
        for items in iters:
            if items.count(items[0]) != N:
                yield items
    else:
        for items in iters:
            vals = tuple(map(key, items))
            if vals.count(vals[0]) != N:
                yield items


def diff(
    a: ArrayLike,
    n=1,
    axis=-1,
    prepend: ArrayLike | None = None,
    append: ArrayLike | None = None,
):
    axis = _util.normalize_axis_index(axis, a.ndim)

    if n < 0:
        raise ValueError(f"order must be non-negative but got {n}")

    if n == 0:
        # match numpy and return the input immediately
        return a

    if prepend is not None:
        shape = list(a.shape)
        shape[axis] = prepend.shape[axis] if prepend.ndim > 0 else 1
        prepend = torch.broadcast_to(prepend, shape)

    if append is not None:
        shape = list(a.shape)
        shape[axis] = append.shape[axis] if append.ndim > 0 else 1
        append = torch.broadcast_to(append, shape)

    return torch.diff(a, n, axis=axis, prepend=prepend, append=append)


def diff(f, *symbols, **kwargs):
    """
    Differentiate f with respect to symbols.

    Explanation
    ===========

    This is just a wrapper to unify .diff() and the Derivative class; its
    interface is similar to that of integrate().  You can use the same
    shortcuts for multiple variables as with Derivative.  For example,
    diff(f(x), x, x, x) and diff(f(x), x, 3) both return the third derivative
    of f(x).

    You can pass evaluate=False to get an unevaluated Derivative class.  Note
    that if there are 0 symbols (such as diff(f(x), x, 0), then the result will
    be the function (the zeroth derivative), even if evaluate=False.

    Examples
    ========

    >>> from sympy import sin, cos, Function, diff
    >>> from sympy.abc import x, y
    >>> f = Function('f')

    >>> diff(sin(x), x)
    cos(x)
    >>> diff(f(x), x, x, x)
    Derivative(f(x), (x, 3))
    >>> diff(f(x), x, 3)
    Derivative(f(x), (x, 3))
    >>> diff(sin(x)*cos(y), x, 2, y, 2)
    sin(x)*cos(y)

    >>> type(diff(sin(x), x))
    cos
    >>> type(diff(sin(x), x, evaluate=False))
    <class 'sympy.core.function.Derivative'>
    >>> type(diff(sin(x), x, 0))
    sin
    >>> type(diff(sin(x), x, 0, evaluate=False))
    sin

    >>> diff(sin(x))
    cos(x)
    >>> diff(sin(x*y))
    Traceback (most recent call last):
    ...
    ValueError: specify differentiation variables to differentiate sin(x*y)

    Note that ``diff(sin(x))`` syntax is meant only for convenience
    in interactive sessions and should be avoided in library code.

    References
    ==========

    .. [1] https://reference.wolfram.com/legacy/v5_2/Built-inFunctions/AlgebraicComputation/Calculus/D.html

    See Also
    ========

    Derivative
    idiff: computes the derivative implicitly

    """
    if hasattr(f, 'diff'):
        return f.diff(*symbols, **kwargs)
    kwargs.setdefault('evaluate', True)
    return _derivative_dispatch(f, *symbols, **kwargs)


def diff(x,order=1,period=None, _cache=_cache):
    """
    Return kth derivative (or integral) of a periodic sequence x.

    If x_j and y_j are Fourier coefficients of periodic functions x
    and y, respectively, then::

      y_j = pow(sqrt(-1)*j*2*pi/period, order) * x_j
      y_0 = 0 if order is not 0.

    Parameters
    ----------
    x : array_like
        Input array.
    order : int, optional
        The order of differentiation. Default order is 1. If order is
        negative, then integration is carried out under the assumption
        that ``x_0 == 0``.
    period : float, optional
        The assumed period of the sequence. Default is ``2*pi``.

    Notes
    -----
    If ``sum(x, axis=0) = 0`` then ``diff(diff(x, k), -k) == x`` (within
    numerical accuracy).

    For odd order and even ``len(x)``, the Nyquist mode is taken zero.

    """  # numpydoc ignore=RT01
    if isinstance(_cache, threading.local):
        if not hasattr(_cache, 'diff_cache'):
            _cache.diff_cache = {}
        _cache = _cache.diff_cache

    tmp = asarray(x)
    if order == 0:
        return tmp
    if iscomplexobj(tmp):
        return diff(tmp.real, order, period, _cache)+1j*diff(
            tmp.imag, order, period, _cache)
    if period is not None:
        c = 2*pi/period
    else:
        c = 1.0
    n = len(x)
    omega = _cache.get((n,order,c))
    if omega is None:
        if len(_cache) > 20:
            while _cache:
                _cache.popitem()

        def kernel(k,order=order,c=c):
            if k:
                return pow(c*k,order)
            return 0
        omega = convolve.init_convolution_kernel(n,kernel,d=order,
                                                 zero_nyquist=1)
        _cache[(n,order,c)] = omega
    overwrite_x = _datacopied(tmp, x)
    return convolve.convolve(tmp,omega,swap_real_imag=order % 2,
                             overwrite_x=overwrite_x)


def diff(
    x: Array,
    /,
    *,
    axis: int = -1,
    n: int = 1,
    prepend: Array | None = None,
    append: Array | None = None,
) -> Array:
    return torch.diff(x, dim=axis, n=n, prepend=prepend, append=append)


def diff(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    return (x2 - x1, y2 - y1)


def diff(arr, n: int | float | np.integer | np.floating, axis: AxisInt = 0):
    """
    difference of n between self,
    analogous to s-s.shift(n)

    Parameters
    ----------
    arr : ndarray or ExtensionArray
    n : int
        number of periods
    axis : {0, 1}
        axis to shift on
    stacklevel : int, default 3
        The stacklevel for the lost dtype warning.

    Returns
    -------
    shifted
    """

    # added a check on the integer value of period
    # see https://github.com/pandas-dev/pandas/issues/56607
    if not lib.is_integer(n):
        if not (is_float(n) and n.is_integer()):
            raise ValueError("periods must be an integer")
        n = int(n)
    na = np.nan
    dtype = arr.dtype

    is_bool = is_bool_dtype(dtype)
    if is_bool:
        op = operator.xor
    else:
        op = operator.sub

    if isinstance(dtype, NumpyEADtype):
        # NumpyExtensionArray cannot necessarily hold shifted versions of itself.
        arr = arr.to_numpy()
        dtype = arr.dtype

    if not isinstance(arr, np.ndarray):
        # i.e ExtensionArray
        if hasattr(arr, f"__{op.__name__}__"):
            if axis != 0:
                raise ValueError(f"cannot diff {type(arr).__name__} on axis={axis}")
            return op(arr, arr.shift(n))
        else:
            raise TypeError(
                f"{type(arr).__name__} has no 'diff' method. "
                "Convert to a suitable dtype prior to calling 'diff'."
            )

    is_timedelta = False
    if arr.dtype.kind in "mM":
        dtype = np.int64
        arr = arr.view("i8")
        na = iNaT
        is_timedelta = True

    elif is_bool:
        # We have to cast in order to be able to hold np.nan
        dtype = np.object_

    elif dtype.kind in "iu":
        # We have to cast in order to be able to hold np.nan

        # int8, int16 are incompatible with float64,
        # see https://github.com/cython/cython/issues/2646
        if arr.dtype.name in ["int8", "int16"]:
            dtype = np.float32
        else:
            dtype = np.float64

    orig_ndim = arr.ndim
    if orig_ndim == 1:
        # reshape so we can always use algos.diff_2d
        arr = arr.reshape(-1, 1)
        # TODO: require axis == 0

    dtype = np.dtype(dtype)
    out_arr = np.empty(arr.shape, dtype=dtype)

    na_indexer = [slice(None)] * 2
    na_indexer[axis] = slice(None, n) if n >= 0 else slice(n, None)
    out_arr[tuple(na_indexer)] = na

    if arr.dtype.name in _diff_special:
        # TODO: can diff_2d dtype specialization troubles be fixed by defining
        #  out_arr inside diff_2d?
        algos.diff_2d(arr, out_arr, int(n), axis, datetimelike=is_timedelta)
    else:
        # To keep mypy happy, _res_indexer is a list while res_indexer is
        #  a tuple, ditto for lag_indexer.
        _res_indexer = [slice(None)] * 2
        _res_indexer[axis] = slice(n, None) if n >= 0 else slice(None, n)
        res_indexer = tuple(_res_indexer)

        _lag_indexer = [slice(None)] * 2
        _lag_indexer[axis] = slice(None, -n) if n > 0 else slice(-n, None)
        lag_indexer = tuple(_lag_indexer)

        out_arr[res_indexer] = op(arr[res_indexer], arr[lag_indexer])

    if is_timedelta:
        out_arr = out_arr.view("timedelta64[ns]")

    if orig_ndim == 1:
        out_arr = out_arr[:, 0]
    return out_arr


def diff(a, n=1, axis=-1, prepend=np._NoValue, append=np._NoValue):
    """
    Calculate the n-th discrete difference along the given axis.

    The first difference is given by ``out[i] = a[i+1] - a[i]`` along
    the given axis, higher differences are calculated by using `diff`
    recursively.

    Parameters
    ----------
    a : array_like
        Input array
    n : int, optional
        The number of times values are differenced. If zero, the input
        is returned as-is.
    axis : int, optional
        The axis along which the difference is taken, default is the
        last axis.
    prepend, append : array_like, optional
        Values to prepend or append to `a` along axis prior to
        performing the difference.  Scalar values are expanded to
        arrays with length 1 in the direction of axis and the shape
        of the input array in along all other axes.  Otherwise the
        dimension and shape must match `a` except along axis.

    Returns
    -------
    diff : ndarray
        The n-th differences. The shape of the output is the same as `a`
        except along `axis` where the dimension is smaller by `n`. The
        type of the output is the same as the type of the difference
        between any two elements of `a`. This is the same as the type of
        `a` in most cases. A notable exception is `datetime64`, which
        results in a `timedelta64` output array.

    See Also
    --------
    gradient, ediff1d, cumsum

    Notes
    -----
    Type is preserved for boolean arrays, so the result will contain
    `False` when consecutive elements are the same and `True` when they
    differ.

    For unsigned integer arrays, the results will also be unsigned. This
    should not be surprising, as the result is consistent with
    calculating the difference directly:

    >>> u8_arr = np.array([1, 0], dtype=np.uint8)
    >>> np.diff(u8_arr)
    array([255], dtype=uint8)
    >>> u8_arr[1,...] - u8_arr[0,...]
    np.uint8(255)

    If this is not desirable, then the array should be cast to a larger
    integer type first:

    >>> i16_arr = u8_arr.astype(np.int16)
    >>> np.diff(i16_arr)
    array([-1], dtype=int16)

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([1, 2, 4, 7, 0])
    >>> np.diff(x)
    array([ 1,  2,  3, -7])
    >>> np.diff(x, n=2)
    array([  1,   1, -10])

    >>> x = np.array([[1, 3, 6, 10], [0, 5, 6, 8]])
    >>> np.diff(x)
    array([[2, 3, 4],
           [5, 1, 2]])
    >>> np.diff(x, axis=0)
    array([[-1,  2,  0, -2]])

    >>> x = np.arange('1066-10-13', '1066-10-16', dtype=np.datetime64)
    >>> np.diff(x)
    array([1, 1], dtype='timedelta64[D]')

    """
    if n == 0:
        return a
    if n < 0:
        raise ValueError(
            "order must be non-negative but got " + repr(n))

    a = asanyarray(a)
    nd = a.ndim
    if nd == 0:
        raise ValueError("diff requires input that is at least one dimensional")
    axis = normalize_axis_index(axis, nd)

    combined = []
    if prepend is not np._NoValue:
        prepend = np.asanyarray(prepend)
        if prepend.ndim == 0:
            shape = list(a.shape)
            shape[axis] = 1
            prepend = np.broadcast_to(prepend, tuple(shape))
        combined.append(prepend)

    combined.append(a)

    if append is not np._NoValue:
        append = np.asanyarray(append)
        if append.ndim == 0:
            shape = list(a.shape)
            shape[axis] = 1
            append = np.broadcast_to(append, tuple(shape))
        combined.append(append)

    if len(combined) > 1:
        a = np.concatenate(combined, axis)

    slice1 = [slice(None)] * nd
    slice2 = [slice(None)] * nd
    slice1[axis] = slice(1, None)
    slice2[axis] = slice(None, -1)
    slice1 = tuple(slice1)
    slice2 = tuple(slice2)

    op = not_equal if a.dtype == np.bool else subtract
    for _ in range(n):
        a = op(a[slice1], a[slice2])

    return a


def diff(a, /, n=1, axis=-1, prepend=np._NoValue, append=np._NoValue):
    """
    Calculate the n-th discrete difference along the given axis.
    The first difference is given by ``out[i] = a[i+1] - a[i]`` along
    the given axis, higher differences are calculated by using `diff`
    recursively.
    Preserves the input mask.

    Parameters
    ----------
    a : array_like
        Input array
    n : int, optional
        The number of times values are differenced. If zero, the input
        is returned as-is.
    axis : int, optional
        The axis along which the difference is taken, default is the
        last axis.
    prepend, append : array_like, optional
        Values to prepend or append to `a` along axis prior to
        performing the difference.  Scalar values are expanded to
        arrays with length 1 in the direction of axis and the shape
        of the input array in along all other axes.  Otherwise the
        dimension and shape must match `a` except along axis.

    Returns
    -------
    diff : MaskedArray
        The n-th differences. The shape of the output is the same as `a`
        except along `axis` where the dimension is smaller by `n`. The
        type of the output is the same as the type of the difference
        between any two elements of `a`. This is the same as the type of
        `a` in most cases. A notable exception is `datetime64`, which
        results in a `timedelta64` output array.

    See Also
    --------
    numpy.diff : Equivalent function in the top-level NumPy module.

    Notes
    -----
    Type is preserved for boolean arrays, so the result will contain
    `False` when consecutive elements are the same and `True` when they
    differ.

    For unsigned integer arrays, the results will also be unsigned. This
    should not be surprising, as the result is consistent with
    calculating the difference directly:

    >>> u8_arr = np.array([1, 0], dtype=np.uint8)
    >>> np.ma.diff(u8_arr)
    masked_array(data=[255],
                 mask=False,
           fill_value=np.uint64(999999),
                dtype=uint8)
    >>> u8_arr[1,...] - u8_arr[0,...]
    np.uint8(255)

    If this is not desirable, then the array should be cast to a larger
    integer type first:

    >>> i16_arr = u8_arr.astype(np.int16)
    >>> np.ma.diff(i16_arr)
    masked_array(data=[-1],
                 mask=False,
           fill_value=np.int64(999999),
                dtype=int16)

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([1, 2, 3, 4, 7, 0, 2, 3])
    >>> x = np.ma.masked_where(a < 2, a)
    >>> np.ma.diff(x)
    masked_array(data=[--, 1, 1, 3, --, --, 1],
            mask=[ True, False, False, False,  True,  True, False],
        fill_value=999999)

    >>> np.ma.diff(x, n=2)
    masked_array(data=[--, 0, 2, --, --, --],
                mask=[ True, False, False,  True,  True,  True],
        fill_value=999999)

    >>> a = np.array([[1, 3, 1, 5, 10], [0, 1, 5, 6, 8]])
    >>> x = np.ma.masked_equal(a, value=1)
    >>> np.ma.diff(x)
    masked_array(
        data=[[--, --, --, 5],
                [--, --, 1, 2]],
        mask=[[ True,  True,  True, False],
                [ True,  True, False, False]],
        fill_value=1)

    >>> np.ma.diff(x, axis=0)
    masked_array(data=[[--, --, --, 1, -2]],
            mask=[[ True,  True,  True, False, False]],
        fill_value=1)

    """
    if n == 0:
        return a
    if n < 0:
        raise ValueError("order must be non-negative but got " + repr(n))

    a = np.ma.asanyarray(a)
    if a.ndim == 0:
        raise ValueError(
            "diff requires input that is at least one dimensional"
            )

    combined = []
    if prepend is not np._NoValue:
        prepend = np.ma.asanyarray(prepend)
        if prepend.ndim == 0:
            shape = list(a.shape)
            shape[axis] = 1
            prepend = np.broadcast_to(prepend, tuple(shape))
        combined.append(prepend)

    combined.append(a)

    if append is not np._NoValue:
        append = np.ma.asanyarray(append)
        if append.ndim == 0:
            shape = list(a.shape)
            shape[axis] = 1
            append = np.broadcast_to(append, tuple(shape))
        combined.append(append)

    if len(combined) > 1:
        a = np.ma.concatenate(combined, axis)

    # GH 22465 np.diff without prepend/append preserves the mask
    return np.diff(a, n, axis)


def diff(ctx, f, x, n=1, **options):
    r"""
    Numerically computes the derivative of `f`, `f'(x)`, or generally for
    an integer `n \ge 0`, the `n`-th derivative `f^{(n)}(x)`.
    A few basic examples are::

        >>> from mpmath import *
        >>> mp.dps = 15; mp.pretty = True
        >>> diff(lambda x: x**2 + x, 1.0)
        3.0
        >>> diff(lambda x: x**2 + x, 1.0, 2)
        2.0
        >>> diff(lambda x: x**2 + x, 1.0, 3)
        0.0
        >>> nprint([diff(exp, 3, n) for n in range(5)])   # exp'(x) = exp(x)
        [20.0855, 20.0855, 20.0855, 20.0855, 20.0855]

    Even more generally, given a tuple of arguments `(x_1, \ldots, x_k)`
    and order `(n_1, \ldots, n_k)`, the partial derivative
    `f^{(n_1,\ldots,n_k)}(x_1,\ldots,x_k)` is evaluated. For example::

        >>> diff(lambda x,y: 3*x*y + 2*y - x, (0.25, 0.5), (0,1))
        2.75
        >>> diff(lambda x,y: 3*x*y + 2*y - x, (0.25, 0.5), (1,1))
        3.0

    **Options**

    The following optional keyword arguments are recognized:

    ``method``
        Supported methods are ``'step'`` or ``'quad'``: derivatives may be
        computed using either a finite difference with a small step
        size `h` (default), or numerical quadrature.
    ``direction``
        Direction of finite difference: can be -1 for a left
        difference, 0 for a central difference (default), or +1
        for a right difference; more generally can be any complex number.
    ``addprec``
        Extra precision for `h` used to account for the function's
        sensitivity to perturbations (default = 10).
    ``relative``
        Choose `h` relative to the magnitude of `x`, rather than an
        absolute value; useful for large or tiny `x` (default = False).
    ``h``
        As an alternative to ``addprec`` and ``relative``, manually
        select the step size `h`.
    ``singular``
        If True, evaluation exactly at the point `x` is avoided; this is
        useful for differentiating functions with removable singularities.
        Default = False.
    ``radius``
        Radius of integration contour (with ``method = 'quad'``).
        Default = 0.25. A larger radius typically is faster and more
        accurate, but it must be chosen so that `f` has no
        singularities within the radius from the evaluation point.

    A finite difference requires `n+1` function evaluations and must be
    performed at `(n+1)` times the target precision. Accordingly, `f` must
    support fast evaluation at high precision.

    With integration, a larger number of function evaluations is
    required, but not much extra precision is required. For high order
    derivatives, this method may thus be faster if f is very expensive to
    evaluate at high precision.

    **Further examples**

    The direction option is useful for computing left- or right-sided
    derivatives of nonsmooth functions::

        >>> diff(abs, 0, direction=0)
        0.0
        >>> diff(abs, 0, direction=1)
        1.0
        >>> diff(abs, 0, direction=-1)
        -1.0

    More generally, if the direction is nonzero, a right difference
    is computed where the step size is multiplied by sign(direction).
    For example, with direction=+j, the derivative from the positive
    imaginary direction will be computed::

        >>> diff(abs, 0, direction=j)
        (0.0 - 1.0j)

    With integration, the result may have a small imaginary part
    even even if the result is purely real::

        >>> diff(sqrt, 1, method='quad')    # doctest:+ELLIPSIS
        (0.5 - 4.59...e-26j)
        >>> chop(_)
        0.5

    Adding precision to obtain an accurate value::

        >>> diff(cos, 1e-30)
        0.0
        >>> diff(cos, 1e-30, h=0.0001)
        -9.99999998328279e-31
        >>> diff(cos, 1e-30, addprec=100)
        -1.0e-30

    """
    partial = False
    try:
        orders = list(n)
        x = list(x)
        partial = True
    except TypeError:
        pass
    if partial:
        x = [ctx.convert(_) for _ in x]
        return _partial_diff(ctx, f, x, orders, options)
    method = options.get('method', 'step')
    if n == 0 and method != 'quad' and not options.get('singular'):
        return f(ctx.convert(x))
    prec = ctx.prec
    try:
        if method == 'step':
            values, norm, workprec = hsteps(ctx, f, x, n, prec, **options)
            ctx.prec = workprec
            v = ctx.difference(values, n) / norm**n
        elif method == 'quad':
            ctx.prec += 10
            radius = ctx.convert(options.get('radius', 0.25))
            def g(t):
                rei = radius*ctx.expj(t)
                z = x + rei
                return f(z) / rei**n
            d = ctx.quadts(g, [0, 2*ctx.pi])
            v = d * ctx.factorial(n) / (2*ctx.pi)
        else:
            raise ValueError("unknown method: %r" % method)
    finally:
        ctx.prec = prec
    return +v


def diff(a: ArrayLike, n: int = 1, axis: int = -1,
         prepend: ArrayLike | None = None,
         append: ArrayLike | None = None) -> Array:
  """Calculate n-th order difference between array elements along a given axis.

  JAX implementation of :func:`numpy.diff`.

  The first order difference is computed by ``a[i+1] - a[i]``, and the n-th order
  difference is computed ``n`` times recursively.

  Args:
    a: input array. Must have ``a.ndim >= 1``.
    n: int, optional, default=1. Order of the difference. Specifies the number
      of times the difference is computed. If n=0, no difference is computed and
      input is returned as is.
    axis: int, optional, default=-1. Specifies the axis along which the difference
      is computed. The difference is computed along ``axis -1`` by default.
    prepend: scalar or array, optional, default=None. Specifies the values to be
      prepended along ``axis`` before computing the difference.
    append: scalar or array, optional, default=None. Specifies the values to be
      appended along ``axis`` before computing the difference.

  Returns:
    An array containing the n-th order difference between the elements of ``a``.

  See also:
    - :func:`jax.numpy.ediff1d`: Computes the differences between consecutive
      elements of an array.
    - :func:`jax.numpy.cumsum`: Computes the cumulative sum of the elements of
      the array along a given axis.
    - :func:`jax.numpy.gradient`: Computes the gradient of an N-dimensional array.

  Examples:
    ``jnp.diff`` computes the first order difference along ``axis``, by default.

    >>> a = jnp.array([[1, 5, 2, 9],
    ...                [3, 8, 7, 4]])
    >>> jnp.diff(a)
    Array([[ 4, -3,  7],
           [ 5, -1, -3]], dtype=int32)

    When ``n = 2``, second order difference is computed along ``axis``.

    >>> jnp.diff(a, n=2)
    Array([[-7, 10],
           [-6, -2]], dtype=int32)

    When ``prepend = 2``, it is prepended to ``a`` along ``axis`` before computing
    the difference.

    >>> jnp.diff(a, prepend=2)
    Array([[-1,  4, -3,  7],
           [ 1,  5, -1, -3]], dtype=int32)

    When ``append = jnp.array([[3],[1]])``, it is appended to ``a`` along ``axis``
    before computing the difference.

    >>> jnp.diff(a, append=jnp.array([[3],[1]]))
    Array([[ 4, -3,  7, -6],
           [ 5, -1, -3, -3]], dtype=int32)
  """
  arr = util.ensure_arraylike("diff", a)
  n = core.concrete_or_error(operator.index, n, "'n' argument of jnp.diff")
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.diff")
  if n == 0:
    return arr
  if n < 0:
    raise ValueError(f"order must be non-negative but got {n}")
  if arr.ndim == 0:
    raise ValueError(f"diff requires input that is at least one dimensional; got {a}")

  nd = arr.ndim
  axis = _canonicalize_axis(axis, nd)

  combined: list[Array] = []
  if prepend is not None:
    prepend = util.ensure_arraylike("diff", prepend)
    if not np.ndim(prepend):
      shape = list(arr.shape)
      shape[axis] = 1
      prepend = broadcast_to(prepend, tuple(shape))
    combined.append(prepend)

  combined.append(arr)

  if append is not None:
    append = util.ensure_arraylike("diff", append)
    if not np.ndim(append):
      shape = list(arr.shape)
      shape[axis] = 1
      append = broadcast_to(append, tuple(shape))
    combined.append(append)

  if len(combined) > 1:
    arr = concatenate(combined, axis)

  slice1 = [slice(None)] * nd
  slice2 = [slice(None)] * nd
  slice1[axis] = slice(1, None)
  slice2[axis] = slice(None, -1)
  slice1_tuple = tuple(slice1)
  slice2_tuple = tuple(slice2)

  op = operator.ne if arr.dtype == np.bool_ else operator.sub
  for _ in range(n):
    arr = op(arr[slice1_tuple], arr[slice2_tuple])

  return arr

