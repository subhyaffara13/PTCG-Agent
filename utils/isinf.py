import re

def isinf(x):
    if is_integer_type(x):
        return full_like(x, False, dtype=torch.bool)
    fn = ops_wrapper("isinf")
    return make_pointwise(fn, override_return_dtype=torch.bool)(x)


def isinf(a: TensorLikeType) -> TensorLikeType:
    if utils.is_complex_dtype(a.dtype):
        return torch.logical_or(isinf(torch.real(a)), isinf(torch.imag(a)))
    if utils.is_float_dtype(a.dtype):
        return torch.abs(a) == float("inf")
    return torch.zeros_like(a, dtype=torch.bool)


def isinf(g: jit_utils.GraphContext, input):
    return g.op("IsInf", g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.DOUBLE))


def isinf(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return IsInfOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def isinf(x: ArrayLike, /) -> Array:
  """Return a boolean array indicating whether each element of input is infinite.

  JAX implementation of :obj:`numpy.isinf`.

  Args:
    x: input array or scalar.

  Returns:
    A boolean array of same shape as ``x`` containing ``True`` where ``x`` is
    ``inf`` or ``-inf``, and ``False`` otherwise.

  See also:
    - :func:`jax.numpy.isposinf`: Returns a boolean array indicating whether each
      element of input is positive infinity.
    - :func:`jax.numpy.isneginf`: Returns a boolean array indicating whether each
      element of input is negative infinity.
    - :func:`jax.numpy.isfinite`: Returns a boolean array indicating whether each
      element of input is finite.
    - :func:`jax.numpy.isnan`: Returns a boolean array indicating whether each
      element of input is not a number (``NaN``).

  Examples:
    >>> jnp.isinf(jnp.inf)
    Array(True, dtype=bool)
    >>> x = jnp.array([2+3j, -jnp.inf, 6, jnp.inf, jnp.nan])
    >>> jnp.isinf(x)
    Array([False,  True, False,  True, False], dtype=bool)
  """
  x = ensure_arraylike("isinf", x)
  dtype = x.dtype
  if dtypes.issubdtype(dtype, np.floating):
    return lax.eq(lax.abs(x), _constant_like(x, np.inf))
  elif dtypes.issubdtype(dtype, np.complexfloating):
    re = lax.real(x)
    im = lax.imag(x)
    return lax.bitwise_or(lax.eq(lax.abs(re), _constant_like(re, np.inf)),
                          lax.eq(lax.abs(im), _constant_like(im, np.inf)))
  else:
    return lax.full_like(x, False, dtype=np.bool_)

