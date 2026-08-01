
def shift_left(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ShiftLeftOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def shift_left(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ShiftLeftOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def shift_left(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise left shift: :math:`x \ll y`.

  This function lowers directly to the `stablehlo.shift_left`_ operation.

  Args:
    x, y: Input arrays. Must have matching integer dtypes. If neither is a
      scalar, ``x`` and ``y`` must have the same number of dimensions and
      be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the element-wise
    left shift of each pair of broadcasted entries.

  See also:
    - :func:`jax.numpy.left_shift`: NumPy wrapper for this API, also accessible
      via the ``x << y`` operator on JAX arrays.
    - :func:`jax.lax.shift_right_arithmetic`: Elementwise arithmetic right shift.
    - :func:`jax.lax.shift_right_logical`: Elementwise logical right shift.

  .. _stablehlo.shift_left: https://openxla.org/stablehlo/spec#shift_left
  """
  x, y = core.auto_insert_reshard(x, y)
  return shift_left_p.bind(x, y)

