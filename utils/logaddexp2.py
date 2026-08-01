
def logaddexp2(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    torch._check(
        not (utils.is_complex_dtype(a.dtype) or utils.is_complex_dtype(b.dtype)),
        lambda: "logaddexp2 doesn't support complex dtypes",
    )
    # Nb. this implementation does not distribute the gradients evenly when a == b
    mask = a >= b
    max_ = torch.where(mask, a, b)
    min_ = torch.where(mask, b, a)
    inf_mask = torch.logical_and(torch.isinf(a), a == b)
    inv_log_2 = 1.0 / math.log(2)
    result = max_ + torch.log1p(torch.exp2(min_ - max_)) * inv_log_2
    return torch.where(inf_mask, a, result)


def logaddexp2(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Compute log2(exp2(x1) + exp2(x2)) avoiding overflow."""
  x1_arr = lax.asarray(x1)
  x2_arr = lax.asarray(x2)
  assert x1_arr.dtype == x2_arr.dtype

  amax = lax.max(x1_arr, x2_arr)
  invln2 = lax._const(amax, 1/np.log(2))
  if dtypes.isdtype(x1_arr.dtype, "real floating"):
    delta = lax.sub(x1_arr, x2_arr)
    return lax.select(lax._isnan(delta),
                      lax.add(x1_arr, x2_arr),  # NaNs or infinities of the same sign.
                      lax.add(amax, lax.mul(invln2, lax.log1p(lax.exp2(lax.neg(lax.abs(delta)))))))
  elif dtypes.isdtype(x1_arr.dtype, "complex floating"):
    delta = lax.sub(lax.add(x1_arr, x2_arr), lax.mul(amax, lax._const(amax, 2)))
    out = lax.add(amax, lax.mul(invln2, lax.log1p(lax.exp2(delta))))
    return lax.complex(lax.real(out), _wrap_between(lax.imag(out), np.pi / np.log(2)))
  else:
    raise ValueError(f"logaddexp2 requires floating-point or complex inputs; got {x1_arr.dtype}")


def logaddexp2(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Logarithm of the sum of exponentials of inputs in base-2 avoiding overflow.

  JAX implementation of :obj:`numpy.logaddexp2`.

  Args:
    x1: input array or scalar.
    x2: input array or scalar. ``x1`` and ``x2`` should either have same shape or
      be broadcast compatible.

  Returns:
    An array containing the result, :math:`log_2(2^{x1}+2^{x2})`, element-wise.

  See also:
    - :func:`jax.numpy.logaddexp`: Computes ``log(exp(x1) + exp(x2))``, element-wise.
    - :func:`jax.numpy.log2`: Calculates the base-2 logarithm of ``x`` element-wise.

  Examples:
    >>> x1 = jnp.array([[3, -1, 4],
    ...                 [8, 5, -2]])
    >>> x2 = jnp.array([2, 3, -5])
    >>> result1 = jnp.logaddexp2(x1, x2)
    >>> result2 = jnp.log2(jnp.exp2(x1) + jnp.exp2(x2))
    >>> jnp.allclose(result1, result2)
    Array(True, dtype=bool)
  """
  x1, x2 = promote_args_inexact("logaddexp2", x1, x2)
  return lax_other.logaddexp2(x1, x2)

