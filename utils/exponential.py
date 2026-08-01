
def exponential(self, rate=1, generator=None):
    if generator is not None:
        raise AssertionError("generator is not supported in refs")
    torch._check(
        not utils.is_complex_dtype(self.dtype)
        and not utils.is_integer_dtype(self.dtype)
        and not utils.is_boolean_dtype(self.dtype),
        lambda: f"Exponential distribution is a continuous probability distribution. \
        dtype must be a floating point but you specified {self.dtype}",
    )
    torch._check(
        rate > 0.0,
        lambda: f"exponential_ expects lambda > 0.0, but found lambda={rate}",
    )

    uniform_val = torch.rand_like(self)

    # copying numerics of transformation::exponential see comment:
    # curand_uniform has (0,1] bounds. log(1) is 0 and exponential excludes 0.
    # we need log to be not 0, and not underflow when converted to half
    # fast __logf approximation can underflow, so set log to -epsilon/2 for 1 or close to 1 args
    epsilon = torch.finfo(uniform_val.dtype).eps / 2
    condition = uniform_val >= 1.0 - epsilon
    log_uniform = torch.where(condition, -epsilon, torch.log(uniform_val))

    return -1 / rate * log_uniform


def exponential(
    M: int,
    *,
    center: float | None = None,
    tau: float = 1.0,
    sym: bool = True,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    requires_grad: bool = False,
) -> Tensor:
    if dtype is None:
        dtype = torch.get_default_dtype()

    _window_function_checks("exponential", M, dtype, layout)

    if tau <= 0:
        raise ValueError(f"Tau must be positive, got: {tau} instead.")

    if sym and center is not None:
        raise ValueError("Center must be None for symmetric windows")

    if M == 0:
        return torch.empty(
            (0,), dtype=dtype, layout=layout, device=device, requires_grad=requires_grad
        )

    if center is None:
        center = (M if not sym and M > 1 else M - 1) / 2.0

    constant = 1 / tau

    k = torch.linspace(
        start=-center * constant,
        end=(-center + (M - 1)) * constant,
        steps=M,
        dtype=dtype,
        layout=layout,
        device=device,
        requires_grad=requires_grad,
    )

    return torch.exp(-torch.abs(k))


def exponential(x, rate):
    return rate*exp(-rate*x)


def Exponential(name, rate):
    r"""
    Create a continuous random variable with an Exponential distribution.

    Explanation
    ===========

    The density of the exponential distribution is given by

    .. math::
        f(x) := \lambda \exp(-\lambda x)

    with $x > 0$. Note that the expected value is `1/\lambda`.

    Parameters
    ==========

    rate : A positive Real number, `\lambda > 0`, the rate (or inverse scale/inverse mean)

    Returns
    =======

    RandomSymbol

    Examples
    ========

    >>> from sympy.stats import Exponential, density, cdf, E
    >>> from sympy.stats import variance, std, skewness, quantile
    >>> from sympy import Symbol

    >>> l = Symbol("lambda", positive=True)
    >>> z = Symbol("z")
    >>> p = Symbol("p")
    >>> X = Exponential("x", l)

    >>> density(X)(z)
    lambda*exp(-lambda*z)

    >>> cdf(X)(z)
    Piecewise((1 - exp(-lambda*z), z >= 0), (0, True))

    >>> quantile(X)(p)
    -log(1 - p)/lambda

    >>> E(X)
    1/lambda

    >>> variance(X)
    lambda**(-2)

    >>> skewness(X)
    2

    >>> X = Exponential('x', 10)

    >>> density(X)(z)
    10*exp(-10*z)

    >>> E(X)
    1/10

    >>> std(X)
    1/10

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Exponential_distribution
    .. [2] https://mathworld.wolfram.com/ExponentialDistribution.html

    """

    return rv(name, ExponentialDistribution, (rate, ))


def exponential(M, center=None, tau=1., sym=True, *, xp=None, device=None):
    r"""Return an exponential (or Poisson) window.

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero, an empty array
        is returned. An exception is thrown when it is negative.
    center : float, optional
        Parameter defining the center location of the window function.
        The default value if not given is ``center = (M-1) / 2``.  This
        parameter must take its default value for symmetric windows.
    tau : float, optional
        Parameter defining the decay.  For ``center = 0`` use
        ``tau = -(M-1) / ln(x)`` if ``x`` is the fraction of the window
        remaining at the end.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.
    %(xp_device_snippet)s

    Returns
    -------
    w : ndarray
        The window, with the maximum value normalized to 1 (though the value 1
        does not appear if `M` is even and `sym` is True).

    Notes
    -----
    The Exponential window is defined as

    .. math::  w(n) = e^{-|n-center| / \tau}

    References
    ----------
    .. [1] S. Gade and H. Herlufsen, "Windows to FFT analysis (Part I)",
           Technical Review 3, Bruel & Kjaer, 1987.

    Examples
    --------
    Plot the symmetric window and its frequency response:

    >>> import numpy as np
    >>> from scipy import signal
    >>> from scipy.fft import fft, fftshift
    >>> import matplotlib.pyplot as plt

    >>> M = 51
    >>> tau = 3.0
    >>> window = signal.windows.exponential(M, tau=tau)
    >>> plt.plot(window)
    >>> plt.title("Exponential Window (tau=3.0)")
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")

    >>> plt.figure()
    >>> A = fft(window, 2048) / (len(window)/2.0)
    >>> freq = np.linspace(-0.5, 0.5, len(A))
    >>> response = 20 * np.log10(np.abs(fftshift(A / abs(A).max())))
    >>> plt.plot(freq, response)
    >>> plt.axis([-0.5, 0.5, -35, 0])
    >>> plt.title("Frequency response of the Exponential window (tau=3.0)")
    >>> plt.ylabel("Normalized magnitude [dB]")
    >>> plt.xlabel("Normalized frequency [cycles per sample]")

    This function can also generate non-symmetric windows:

    >>> tau2 = -(M-1) / np.log(0.01)
    >>> window2 = signal.windows.exponential(M, 0, tau2, False)
    >>> plt.figure()
    >>> plt.plot(window2)
    >>> plt.ylabel("Amplitude")
    >>> plt.xlabel("Sample")
    """
    xp = _namespace(xp)

    if sym and center is not None:
        raise ValueError("If sym==True, center must be None.")
    if _len_guards(M):
        return xp.ones(M, dtype=xp.float64, device=device)
    M, needs_trunc = _extend(M, sym)

    if center is None:
        center = (M-1) / 2

    n = xp.arange(0, M, dtype=xp.float64, device=device)
    w = xp.exp(-abs(n-center) / tau)

    return _truncate(w, needs_trunc)


def exponential(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ExpOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def exponential(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ExpOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def exponential(key: ArrayLike,
                shape: Shape = (),
                dtype: DTypeLikeFloat | None = None,
                *,
                out_sharding: NamedSharding | P | None = None) -> Array:
  r"""Sample Exponential random values with given shape and float dtype.

  The values are distributed according to the probability density function:

  .. math::
     f(x) = e^{-x}

  on the domain :math:`0 \le x < \infty`.

  Args:
    key: a PRNG key used as the random key.
    shape: optional, a tuple of nonnegative integers representing the result
      shape. Default ().
    dtype: optional, a float dtype for the returned values (default float64 if
      jax_enable_x64 is true, otherwise float32).
    out_sharding: Optional. Specifies how the output array should be sharded
      across devices in multi-device computation. Can be a
      :class:`~jax.sharding.NamedSharding`, a :class:`~jax.sharding.PartitionSpec`
      (``P``), or ``None`` (default). When specified, the output will be sharded
      according to the given sharding specification. Primarily used in explicit
      sharding mode.
      See the `explicit sharding tutorial <https://docs.jax.dev/en/latest/parallel.html>`_
      for more details.

  Returns:
    A random array with the specified shape and dtype.
  """
  key, _ = _check_prng_key("exponential", key)
  dtype = dtypes.check_and_canonicalize_user_dtype(
      float if dtype is None else dtype)
  if not dtypes.issubdtype(dtype, np.floating):
    raise ValueError(f"dtype argument to `exponential` must be a float "
                     f"dtype, got {dtype}")
  shape = core.canonicalize_shape(shape)
  out_sharding = canonicalize_sharding_for_samplers(out_sharding, "exponential", shape)
  return maybe_auto_axes(_exponential, out_sharding,
                         shape=shape, dtype=dtype)(key)

