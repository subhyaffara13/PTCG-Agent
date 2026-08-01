
def multigammaln(a: TensorLikeType, p: int) -> TensorLikeType:
    c = 0.25 * p * (p - 1) * math.log(math.pi)
    b = 0.5 * torch.arange(start=(1 - p), end=1, step=1, dtype=a.dtype, device=a.device)
    return torch.sum(torch.lgamma(a.unsqueeze(-1) + b), dim=-1) + c


def multigammaln(a, d):
    r"""Returns the log of multivariate gamma, also sometimes called the
    generalized gamma.

    Parameters
    ----------
    a : ndarray
        The multivariate gamma is computed for each item of `a`.
    d : int
        The dimension of the space of integration.

    Returns
    -------
    res : ndarray
        The values of the log multivariate gamma at the given points `a`.

    Notes
    -----
    The formal definition of the multivariate gamma of dimension d for a real
    `a` is

    .. math::

        \Gamma_d(a) = \int_{A>0} e^{-tr(A)} |A|^{a - (d+1)/2} dA

    with the condition :math:`a > (d-1)/2`, and :math:`A > 0` being the set of
    all the positive definite matrices of dimension `d`.  Note that `a` is a
    scalar: the integrand only is multivariate, the argument is not (the
    function is defined over a subset of the real set).

    This can be proven to be equal to the much friendlier equation

    .. math::

        \Gamma_d(a) = \pi^{d(d-1)/4} \prod_{i=1}^{d} \Gamma(a - (i-1)/2).

    References
    ----------
    R. J. Muirhead, Aspects of multivariate statistical theory (Wiley Series in
    probability and mathematical statistics).

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.special import multigammaln, gammaln
    >>> a = 23.5
    >>> d = 10
    >>> multigammaln(a, d)
    454.1488605074416

    Verify that the result agrees with the logarithm of the equation
    shown above:

    >>> d*(d-1)/4*np.log(np.pi) + gammaln(a - 0.5*np.arange(0, d)).sum()
    454.1488605074416
    """
    a = np.asarray(a)
    # Support for 0d arrays is needed for array_api_strict and dask.
    d = np.asarray(d)[()]
    if not np.isscalar(d) or (np.floor(d) != d):
        raise ValueError("d should be a positive integer (dimension)")
    if np.any(a <= 0.5 * (d - 1)):
        raise ValueError(f"condition a ({a}) > 0.5 * (d-1) ({0.5 * (d-1)}) not met")

    res = (d * (d-1) * 0.25) * np.log(np.pi)
    res += np.sum(loggam([(a - (j - 1.)/2) for j in range(1, d+1)]), axis=0)
    return res


def multigammaln(a: ArrayLike, d: ArrayLike) -> Array:
  r"""The natural log of the multivariate gamma function.

  JAX implementation of :func:`scipy.special.multigammaln`.

  .. math::

     \mathrm{multigammaln}(a, d) = \log\Gamma_d(a)

  where

  .. math::

     \Gamma_d(a) = \pi^{d(d-1)/4}\prod_{i=1}^d\Gamma(a-(i-1)/2)

  and :math:`\Gamma(x)` is the :func:`~jax.scipy.special.gamma` function.

  Args:
    a: arraylike, real-valued.
    d: int, the dimension of the integration space.

  Returns:
    array containing values of the log-multigamma function.

  See also:
    - :func:`jax.scipy.special.gamma`
  """
  d = core.concrete_or_error(int, d, "d argument of multigammaln")
  a, d_ = promote_args_inexact("multigammaln", a, d)

  constant = lax.mul(lax.mul(lax.mul(_lax_const(a, 0.25), d_),
                             lax.sub(d_, _lax_const(a, 1))),
                     lax.log(_lax_const(a, np.pi)))
  b = lax.div(jnp.arange(d, dtype=d_.dtype), _lax_const(a, 2))
  res = jnp.sum(gammaln(jnp.expand_dims(a, axis=-1) -
                        jnp.expand_dims(b, axis=tuple(range(a.ndim)))),
                axis=-1)
  return res + constant

