
def sinc(x: ArrayLike):
    return torch.sinc(x)


def sinc(a):
    a = math.pi * a
    return torch.where(a == 0, 1, torch.sin(a) / a)


def sinc(x: Array, /, *, xp: ModuleType | None = None) -> Array:
    r"""
    Return the normalized sinc function.

    The sinc function is equal to :math:`\sin(\pi x)/(\pi x)` for any argument
    :math:`x\ne 0`. ``sinc(0)`` takes the limit value 1, making ``sinc`` not
    only everywhere continuous but also infinitely differentiable.

    .. note::

        Note the normalization factor of ``pi`` used in the definition.
        This is the most commonly used definition in signal processing.
        Use ``sinc(x / xp.pi)`` to obtain the unnormalized sinc function
        :math:`\sin(x)/x` that is more common in mathematics.

    Parameters
    ----------
    x : array
        Array (possibly multi-dimensional) of values for which to calculate
        ``sinc(x)``. Must have a real floating point dtype.
    xp : array_namespace, optional
        The standard-compatible namespace for `x`. Default: infer.

    Returns
    -------
    array
        ``sinc(x)`` calculated elementwise, which has the same shape as the input.

    Notes
    -----
    The name sinc is short for "sine cardinal" or "sinus cardinalis".

    The sinc function is used in various signal processing applications,
    including in anti-aliasing, in the construction of a Lanczos resampling
    filter, and in interpolation.

    For bandlimited interpolation of discrete-time signals, the ideal
    interpolation kernel is proportional to the sinc function.

    References
    ----------
    #. Weisstein, Eric W. "Sinc Function." From MathWorld--A Wolfram Web
       Resource. https://mathworld.wolfram.com/SincFunction.html
    #. Wikipedia, "Sinc function",
       https://en.wikipedia.org/wiki/Sinc_function

    Examples
    --------
    >>> import array_api_strict as xp
    >>> import array_api_extra as xpx
    >>> x = xp.linspace(-4, 4, 41)
    >>> xpx.sinc(x, xp=xp)
    Array([-3.89817183e-17, -4.92362781e-02,
           -8.40918587e-02, -8.90384387e-02,
           -5.84680802e-02,  3.89817183e-17,
            6.68206631e-02,  1.16434881e-01,
            1.26137788e-01,  8.50444803e-02,
           -3.89817183e-17, -1.03943254e-01,
           -1.89206682e-01, -2.16236208e-01,
           -1.55914881e-01,  3.89817183e-17,
            2.33872321e-01,  5.04551152e-01,
            7.56826729e-01,  9.35489284e-01,
            1.00000000e+00,  9.35489284e-01,
            7.56826729e-01,  5.04551152e-01,
            2.33872321e-01,  3.89817183e-17,
           -1.55914881e-01, -2.16236208e-01,
           -1.89206682e-01, -1.03943254e-01,
           -3.89817183e-17,  8.50444803e-02,
            1.26137788e-01,  1.16434881e-01,
            6.68206631e-02,  3.89817183e-17,
           -5.84680802e-02, -8.90384387e-02,
           -8.40918587e-02, -4.92362781e-02,
           -3.89817183e-17], dtype=array_api_strict.float64)
    """

    if xp is None:
        xp = array_namespace(x)

    if not xp.isdtype(x.dtype, "real floating"):
        err_msg = "`x` must have a real floating data type."
        raise ValueError(err_msg)

    if (
        is_numpy_namespace(xp)
        or is_cupy_namespace(xp)
        or is_jax_namespace(xp)
        or is_torch_namespace(xp)
        or is_dask_namespace(xp)
    ):
        return xp.sinc(x)

    return _funcs.sinc(x, xp=xp)


def sinc(x: Array, /, *, xp: ModuleType) -> Array:
    # numpydoc ignore=PR01,RT01
    """See docstring in `array_api_extra._delegation.py`."""

    # no scalars in `where` - array-api#807
    y = xp.pi * xp.where(
        xp.astype(x, xp.bool),
        x,
        xp.asarray(xp.finfo(x.dtype).eps, dtype=x.dtype, device=_compat.device(x)),
    )
    return xp.sin(y) / y


def sinc(x):
    r"""
    Return the normalized sinc function.

    The sinc function is equal to :math:`\sin(\pi x)/(\pi x)` for any argument
    :math:`x\ne 0`. ``sinc(0)`` takes the limit value 1, making ``sinc`` not
    only everywhere continuous but also infinitely differentiable.

    .. note::

        Note the normalization factor of ``pi`` used in the definition.
        This is the most commonly used definition in signal processing.
        Use ``sinc(x / np.pi)`` to obtain the unnormalized sinc function
        :math:`\sin(x)/x` that is more common in mathematics.

    Parameters
    ----------
    x : ndarray
        Array (possibly multi-dimensional) of values for which to calculate
        ``sinc(x)``.

    Returns
    -------
    out : ndarray
        ``sinc(x)``, which has the same shape as the input.

    Notes
    -----
    The name sinc is short for "sine cardinal" or "sinus cardinalis".

    The sinc function is used in various signal processing applications,
    including in anti-aliasing, in the construction of a Lanczos resampling
    filter, and in interpolation.

    For bandlimited interpolation of discrete-time signals, the ideal
    interpolation kernel is proportional to the sinc function.

    References
    ----------
    .. [1] Weisstein, Eric W. "Sinc Function." From MathWorld--A Wolfram Web
           Resource. https://mathworld.wolfram.com/SincFunction.html
    .. [2] Wikipedia, "Sinc function",
           https://en.wikipedia.org/wiki/Sinc_function

    Examples
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> x = np.linspace(-4, 4, 41)
    >>> np.sinc(x)
     array([-3.89804309e-17,  -4.92362781e-02,  -8.40918587e-02, # may vary
            -8.90384387e-02,  -5.84680802e-02,   3.89804309e-17,
            6.68206631e-02,   1.16434881e-01,   1.26137788e-01,
            8.50444803e-02,  -3.89804309e-17,  -1.03943254e-01,
            -1.89206682e-01,  -2.16236208e-01,  -1.55914881e-01,
            3.89804309e-17,   2.33872321e-01,   5.04551152e-01,
            7.56826729e-01,   9.35489284e-01,   1.00000000e+00,
            9.35489284e-01,   7.56826729e-01,   5.04551152e-01,
            2.33872321e-01,   3.89804309e-17,  -1.55914881e-01,
           -2.16236208e-01,  -1.89206682e-01,  -1.03943254e-01,
           -3.89804309e-17,   8.50444803e-02,   1.26137788e-01,
            1.16434881e-01,   6.68206631e-02,   3.89804309e-17,
            -5.84680802e-02,  -8.90384387e-02,  -8.40918587e-02,
            -4.92362781e-02,  -3.89804309e-17])

    >>> plt.plot(x, np.sinc(x))
    [<matplotlib.lines.Line2D object at 0x...>]
    >>> plt.title("Sinc Function")
    Text(0.5, 1.0, 'Sinc Function')
    >>> plt.ylabel("Amplitude")
    Text(0, 0.5, 'Amplitude')
    >>> plt.xlabel("X")
    Text(0.5, 0, 'X')
    >>> plt.show()

    """
    x = np.asanyarray(x)
    x = pi * x
    # Hope that 1e-20 is sufficient for objects...
    eps = np.finfo(x.dtype).eps if x.dtype.kind == "f" else 1e-20
    y = where(x, x, eps)
    return sin(y) / y


def sinc(ctx, x):
    if ctx.isinf(x):
        return 1/x
    if not x:
        return x+1
    return ctx.sin(x)/x


def sinc(x: ArrayLike, /) -> Array:
  r"""Calculate the normalized sinc function.

  JAX implementation of :func:`numpy.sinc`.

  The normalized sinc function is given by

  .. math::
     \mathrm{sinc}(x) = \frac{\sin({\pi x})}{\pi x}

  where ``sinc(0)`` returns the limit value of ``1``. The sinc function is
  smooth and infinitely differentiable.

  Args:
    x : input array; will be promoted to an inexact type.

  Returns:
    An array of the same shape as ``x`` containing the result.

  Examples:
    >>> x = jnp.array([-1, -0.5, 0, 0.5, 1])
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.sinc(x)
    Array([-0.   ,  0.637,  1.   ,  0.637, -0.   ], dtype=float32)

    Compare this to the naive approach to computing the function, which is
    undefined at zero:

    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   jnp.sin(jnp.pi * x) / (jnp.pi * x)
    Array([-0.   ,  0.637,    nan,  0.637, -0.   ], dtype=float32)

    JAX defines a custom gradient rule for sinc to allow accurate evaluation
    of the gradient at zero even for higher-order derivatives:

    >>> f = jnp.sinc
    >>> for i in range(1, 6):
    ...   f = jax.grad(f)
    ...   print(f"(d/dx)^{i} f(0.0) = {f(0.0):.2f}")
    ...
    (d/dx)^1 f(0.0) = 0.00
    (d/dx)^2 f(0.0) = -3.29
    (d/dx)^3 f(0.0) = 0.00
    (d/dx)^4 f(0.0) = 19.48
    (d/dx)^5 f(0.0) = 0.00
  """
  x = ensure_arraylike("sinc", x)
  x, = promote_dtypes_inexact(x)
  eq_zero = lax.eq(x, _lax_const(x, 0))
  pi_x = lax.mul(_lax_const(x, np.pi), x)
  safe_pi_x = _where(eq_zero, _lax_const(x, 1), pi_x)
  return _where(eq_zero, _sinc_maclaurin(0, pi_x),
                lax.div(lax.sin(safe_pi_x), safe_pi_x))

