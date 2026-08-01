
def is_finite(x: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return IsFiniteOp(x=x, results=results, loc=loc, ip=ip).result


def is_finite(x: _ods_ir.Value[_ods_ir.RankedTensorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return IsFiniteOp(x=x, results=results, loc=loc, ip=ip).result


def is_finite(x: ArrayLike) -> Array:
  r"""Elementwise :math:`\mathrm{isfinite}`.

  This function lowers directly to the  `stablehlo.is_finite`_ operation.

  Args:
    x: input array. Must have floating-point type.

  Returns:
    Array of boolean dtype with the same shape as ``x``, containing ``False`` where
    ``x`` is :math:`\pm\infty` or :math:`\mathit{NaN}`, and ``True`` otherwise.

  See also:
    - :func:`jax.numpy.isinf`: return True where array is infinite.
    - :func:`jax.numpy.isnan`: return True where array is NaN.

  .. _stablehlo.is_finite: https://openxla.org/stablehlo/spec#is_finite
  """
  return is_finite_p.bind(x)

