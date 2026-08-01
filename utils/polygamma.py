
def polygamma(n, x):
    r"""Polygamma functions.

    Defined as :math:`\psi^{(n)}(x)` where :math:`\psi` is the
    `digamma` function. See [dlmf]_ for details.

    Parameters
    ----------
    n : array_like
        The order of the derivative of the digamma function; must be
        integral
    x : array_like
        Real valued input

    Returns
    -------
    ndarray
        Function results

    See Also
    --------
    digamma

    References
    ----------
    .. [dlmf] NIST, Digital Library of Mathematical Functions,
        https://dlmf.nist.gov/5.15

    Examples
    --------
    >>> from scipy import special
    >>> x = [2, 3, 25.5]
    >>> special.polygamma(1, x)
    array([ 0.64493407,  0.39493407,  0.03999467])
    >>> special.polygamma(0, x) == special.psi(x)
    array([ True,  True,  True], dtype=bool)

    """
    n, x = asarray(n), asarray(x)
    fac2 = (-1.0)**(n+1) * gamma(n+1.0) * zeta(n+1, x)
    return where(n == 0, psi(x), fac2)


def polygamma(n: _ods_ir.Value, x: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return PolygammaOp(n=n, x=x, results=results, loc=loc, ip=ip).result


def polygamma(m: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise polygamma: :math:`\psi^{(m)}(x)`."""
  m, x = core.auto_insert_reshard(m, x)
  return polygamma_p.bind(m, x)


def polygamma(n: ArrayLike, x: ArrayLike) -> Array:
  r"""The polygamma function.

  JAX implementation of :func:`scipy.special.polygamma`.

  .. math::

     \mathrm{polygamma}(n, x) = \psi^{(n)}(x) = \frac{\mathrm{d}^{n+1}}{\mathrm{d}x^{n+1}} \log \Gamma(x)

  where :math:`\psi` is the :func:`~jax.scipy.special.digamma` function and
  :math:`\Gamma` is the :func:`~jax.scipy.special.gamma` function.

  Args:
    n: arraylike, integer-valued. The order of the derivative.
    x: arraylike, real-valued. The value at which to evaluate the function.

  Returns:
    array

  See also:
    - :func:`jax.scipy.special.gamma`
    - :func:`jax.scipy.special.digamma`
  """
  if not dtypes.issubdtype(lax.dtype(n), np.integer):
    raise ValueError(
        f"Argument `n` to polygamma must be of integer type. Got dtype {lax.dtype(n)}."
    )
  n_arr, x_arr = promote_args_inexact("polygamma", n, x)
  if dtypes.issubdtype(x_arr.dtype, np.complexfloating):
    raise ValueError("polygamma does not support complex-valued inputs.")
  return lax.polygamma(n_arr, x_arr)

