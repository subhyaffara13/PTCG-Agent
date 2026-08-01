
def remainder(a: TensorLikeType, b: TensorLikeType) -> TensorLikeType:
    return prims.remainder(a, b)


def remainder(g: jit_utils.GraphContext, input, other):
    if symbolic_helper._is_fp(input) or symbolic_helper._is_fp(other):
        return opset9.remainder(g, input, other)
    return g.op("Mod", input, other, fmod_i=0)


def remainder(g: jit_utils.GraphContext, input, other):
    div = _floor_divide(g, input, other)
    quo = g.op("Mul", div, other)
    return g.op("Sub", input, quo)


def remainder(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RemOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def remainder(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RemOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def remainder(x1: ArrayLike, x2: ArrayLike, /) -> Array:
  """Returns element-wise remainder of the division.

  JAX implementation of :obj:`numpy.remainder`.

  Args:
    x1: scalar or array. Specifies the dividend.
    x2: scalar or array. Specifies the divisor. ``x1`` and ``x2`` should either
      have same shape or be broadcast compatible.

  Returns:
    An array containing the remainder of element-wise division of ``x1`` by
    ``x2`` with same sign as the elements of ``x2``.

  Note:
    The result of ``jnp.remainder`` is equivalent to ``x1 - x2 * jnp.floor(x1 / x2)``.

  See also:
    - :func:`jax.numpy.mod`: Returns the element-wise remainder of the division.
    - :func:`jax.numpy.fmod`: Calculates the element-wise floating-point modulo
      operation.
    - :func:`jax.numpy.divmod`: Calculates the integer quotient and remainder of
      ``x1`` by ``x2``, element-wise.

  Examples:
    >>> x1 = jnp.array([[3, -1, 4],
    ...                 [8, 5, -2]])
    >>> x2 = jnp.array([2, 3, -5])
    >>> jnp.remainder(x1, x2)
    Array([[ 1,  2, -1],
           [ 0,  2, -2]], dtype=int32)
    >>> x1 - x2 * jnp.floor(x1 / x2)
    Array([[ 1.,  2., -1.],
           [ 0.,  2., -2.]], dtype=float32)
  """
  x1, x2 = promote_args_numeric("remainder", x1, x2)
  jnp_error._set_error_if_divide_by_zero(x2)
  zero = _constant_like(x1, 0)
  if dtypes.issubdtype(x2.dtype, np.integer):
    x2 = _where(x2 == 0, lax._ones(x2), x2)
  trunc_mod = lax.rem(x1, x2)
  trunc_mod_not_zero = lax.ne(trunc_mod, zero)
  do_plus = lax.bitwise_and(
      lax.ne(lax.lt(trunc_mod, zero), lax.lt(x2, zero)), trunc_mod_not_zero)
  out = lax.select(do_plus, lax.add(trunc_mod, x2), trunc_mod)
  jnp_error._set_error_if_nan(out)
  return out

