
def rel_entr(pk: np.ndarray, qk: np.ndarray) -> np.ndarray:
    """
    See https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.rel_entr.html#scipy.special.rel_entr.
    Python implementation.
    """
    res = np.empty(pk.shape, dtype=pk.dtype)
    res[:] = pk[:] * np.log(pk[:] / qk[:])
    c2 = (pk == 0) & (qk >= 0)
    res[c2] = 0
    c1 = (pk > 0) & (qk > 0)
    res[~c1] = np.inf
    return res


def rel_entr(
    p: ArrayLike,
    q: ArrayLike,
) -> Array:
  r"""The relative entropy function.

  JAX implementation of :obj:`scipy.special.rel_entr`.

  .. math::

     \mathrm{rel\_entr}(p, q) = \begin{cases}
       p\log(p/q) & p>0,q>0\\
       0 & p=0,q\ge 0\\
       \infty & \mathrm{otherwise}
    \end{cases}

  Args:
    p: arraylike, real-valued.
    q: arraylike, real-valued.

  Returns:
    array of relative entropy values.

  See also:
    - :func:`jax.scipy.special.entr`
    - :func:`jax.scipy.special.kl_div`
  """
  p, q = promote_args_inexact("rel_entr", p, q)
  if dtypes.issubdtype(p.dtype, np.complexfloating):
    raise ValueError("rel_entr does not support complex-valued inputs.")
  zero = _lax_const(p, 0.0)
  both_gt_zero_mask = lax.bitwise_and(lax.gt(p, zero), lax.gt(q, zero))
  one_zero_mask = lax.bitwise_and(lax.eq(p, zero), lax.ge(q, zero))

  safe_p = jnp.where(both_gt_zero_mask, p, 1)
  safe_q = jnp.where(both_gt_zero_mask, q, 1)
  log_val = lax.sub(_xlogx(safe_p), xlogy(safe_p, safe_q))
  result = jnp.where(
      both_gt_zero_mask, log_val, jnp.where(one_zero_mask, zero, np.inf)
  )
  return result

