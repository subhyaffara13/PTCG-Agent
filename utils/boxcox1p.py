
def boxcox1p(x: ArrayLike, lmbda: ArrayLike) -> Array:
  r"""Box-Cox transformation of ``1 + x``.

  JAX implementation of :obj:`scipy.special.boxcox1p`.

  .. math::

     \mathrm{boxcox1p}(x, \lambda) = \begin{cases}
       ((1 + x)^\lambda - 1) / \lambda & \lambda \ne 0 \\
       \log(1 + x) & \lambda = 0
     \end{cases}

  Defined for :math:`x > -1`; returns ``nan`` for ``x <= -1``.

  Args:
    x: arraylike, real-valued, greater than ``-1``.
    lmbda: arraylike, real-valued.

  Returns:
    array containing values of the shifted Box-Cox transform.

  See also:
    :func:`jax.scipy.special.boxcox`
  """
  x, lmbda = promote_args_inexact("boxcox1p", x, lmbda)
  lmbda_is_zero = lmbda == 0
  safe_lmbda = jnp.where(lmbda_is_zero, jnp.ones_like(lmbda), lmbda)
  log1p_x = jnp.log1p(x)
  power_branch = jnp.expm1(safe_lmbda * log1p_x) / safe_lmbda
  return jnp.where(lmbda_is_zero, log1p_x, power_branch)

