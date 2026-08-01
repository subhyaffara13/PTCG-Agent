
def betaln(a: ArrayLike, b: ArrayLike) -> Array:
  r"""Natural log of the absolute value of the beta function

  JAX implementation of :obj:`scipy.special.betaln`.

  .. math::

     \mathrm{betaln}(a, b) = \log B(a, b)

  where :math:`B` is the :func:`~jax.scipy.special.beta` function.

  Args:
    a: arraylike, real-valued.  Parameter *a* of the beta distribution.
    b: arraylike, real-valued.  Parameter *b* of the beta distribution.

  Returns:
    array containing the values of the log-beta function

  See Also:
    :func:`jax.scipy.special.beta`
  """
  a, b = promote_args_inexact("betaln", a, b)
  return _betaln_impl(a, b)


def betaln(a: ArrayLike, b: ArrayLike) -> Array:
    """Compute the log of the beta function.

    Derived from scipy's implementation of `betaln`_.

    This implementation does not handle all branches of the scipy implementation, but is still much more accurate
    than just doing lgamma(a) + lgamma(b) - lgamma(a + b) when inputs are large (> 1M or so).

    .. _betaln:
        https://github.com/scipy/scipy/blob/ef2dee592ba8fb900ff2308b9d1c79e4d6a0ad8b/scipy/special/cdflib/betaln.f
    """
    a, b = promote_args_inexact("betaln", a, b)
    a, b = jnp.minimum(a, b), jnp.maximum(a, b)
    small_b = lax.lgamma(a) + (lax.lgamma(b) - lax.lgamma(a + b))
    large_b = lax.lgamma(a) + algdiv(a, b)
    return jnp.where(b < 8, small_b, large_b)

