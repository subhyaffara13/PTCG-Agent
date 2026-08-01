
def isfinite(a: TensorLikeType) -> TensorLikeType:
    if utils.is_float_dtype(a.dtype) or utils.is_complex_dtype(a.dtype):
        return prims.isfinite(a)

    return ones_like(a, dtype=torch.bool)


def isfinite(g: jit_utils.GraphContext, input):
    inf_node = isinf(g, input)
    nan_node = opset9.isnan(g, input)
    return opset9.__not_(g, opset9.__or_(g, inf_node, nan_node))


def isfinite(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return IsFiniteOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def isfinite(x: ArrayLike, /) -> Array:
  """Return a boolean array indicating whether each element of input is finite.

  JAX implementation of :obj:`numpy.isfinite`.

  Args:
    x: input array or scalar.

  Returns:
    A boolean array of same shape as ``x`` containing ``True`` where ``x`` is
    not ``inf``, ``-inf``, or ``NaN``, and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.isinf`: Returns a boolean array indicating whether each
      element of input is either positive or negative infinity.
    - :func:`jax.numpy.isposinf`: Returns a boolean array indicating whether each
      element of input is positive infinity.
    - :func:`jax.numpy.isneginf`: Returns a boolean array indicating whether each
      element of input is negative infinity.
    - :func:`jax.numpy.isnan`: Returns a boolean array indicating whether each
      element of input is not a number (``NaN``).

  Examples:
    >>> x = jnp.array([-1, 3, jnp.inf, jnp.nan])
    >>> jnp.isfinite(x)
    Array([ True,  True, False, False], dtype=bool)
    >>> jnp.isfinite(3-4j)
    Array(True, dtype=bool, weak_type=True)
  """
  x = ensure_arraylike("isfinite", x)
  dtype = x.dtype
  if dtypes.issubdtype(dtype, np.floating):
    return lax.is_finite(x)
  elif dtypes.issubdtype(dtype, np.complexfloating):
    return lax.bitwise_and(lax.is_finite(real(x)), lax.is_finite(imag(x)))
  else:
    return lax.full_like(x, True, dtype=np.bool_)

