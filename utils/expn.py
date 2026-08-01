
def expn(n: ArrayLike, x: ArrayLike) -> Array:
  r"""Generalized exponential integral function.

  JAX implementation of :obj:`scipy.special.expn`.

  .. math::

     \mathrm{expn}(x) = E_n(x) = x^{n-1}\int_x^\infty\frac{e^{-t}}{t^n}\mathrm{d}t

  Args:
    n: arraylike, real-valued
    x: arraylike, real-valued

  Returns:
    array of expn values

  See also:
    - :func:`jax.scipy.special.expi`
    - :func:`jax.scipy.special.exp1`
  """
  n, x = promote_args_inexact("expn", n, x)
  if dtypes.issubdtype(x.dtype, np.complexfloating):
    raise ValueError("expn does not support complex-valued inputs.")
  _c = _lax_const
  zero = _c(x, 0)
  one = _c(x, 1)
  conds = [
    (n < _c(n, 0)) | (x < zero),
    (x == zero) & (n < _c(n, 2)),
    (x == zero) & (n >= _c(n, 2)),
    (n == _c(n, 0)) & (x >= zero),
    (n >= _c(n, 5000)),
    (x > one),
  ]
  n1 = jnp.where(n == _c(n, 1), n + n, n)
  vals = [
    np.nan,
    np.inf,
    one / n1,  # prevent div by zero
    jnp.exp(-x) / x,
    _expn3,
    _expn2,
    _expn1,
  ]
  ret = jnp.piecewise(x, conds, vals, n=n)
  return ret

