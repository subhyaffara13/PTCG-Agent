
def shift_right_logical(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ShiftRightLogicalOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def shift_right_logical(lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ShiftRightLogicalOp(lhs=lhs, rhs=rhs, results=results, loc=loc, ip=ip).result


def shift_right_logical(x: ArrayLike, y: ArrayLike) -> Array:
  r"""Elementwise logical right shift: :math:`x \gg y`.

  This function lowers directly to the `stablehlo.shift_right_logical`_ operation.

  Args:
    x, y: Input arrays. Must have matching integer dtypes. If neither is a
      scalar, ``x`` and ``y`` must have the same number of dimensions and
      be broadcast compatible.

  Returns:
    An array of the same dtype as ``x`` and ``y`` containing the element-wise
    logical right shift of each pair of broadcasted entries.

  See also:
    - :func:`jax.numpy.right_shift`: NumPy wrapper for this API when applied to
      unsigned integers, also accessible via the ``x >> y`` operator on JAX arrays
      with unsigned integer dtype.
    - :func:`jax.lax.shift_left`: Elementwise left shift.
    - :func:`jax.lax.shift_right_arithmetic`: Elementwise arithmetic right shift.

  .. _stablehlo.shift_right_logical: https://openxla.org/stablehlo/spec#shift_right_logical
  """
  x, y = core.auto_insert_reshard(x, y)
  return shift_right_logical_p.bind(x, y)

