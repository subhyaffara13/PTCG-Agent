
def rsqrt(a):
    return prims.rsqrt(a)


def rsqrt(g: jit_utils.GraphContext, self):
    return g.op(
        "Div", symbolic_helper._if_scalar_type_as(torch.ones(1), self), sqrt(g, self)
    )


def rsqrt(operand: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return RsqrtOp(operand=operand, fastmath=fastmath, results=results, loc=loc, ip=ip).result


def rsqrt(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RsqrtOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def rsqrt(src: _ods_ir.Value, *, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return RsqrtOp(src=src, ftz=ftz, results=results, loc=loc, ip=ip).result


def rsqrt(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RsqrtOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def rsqrt(x: ArrayLike, *, accuracy: Tolerance | AccuracyMode | None = None) -> Array:
  r"""Elementwise reciprocal square root:  :math:`1 \over \sqrt{x}`.

  This function lowers directly to the `stablehlo.rsqrt`_ operation.

  Args:
    x: Input array. Must have floating or complex dtype.
    accuracy: Optional `lax.Tolerance` or `lax.AccuracyMode` object that
      selects the implementation of the op based on the requested accuracy. If
      the implementation cannot satisfy the requested tolerance, the
      compiler will return an error. If mode is specified and there are no
      multiple implementations available, the default implementation will be
      used.

  Returns:
    An array of the same shape and dtype as ``x`` containing the
    reciporical square root.

  See also:
    :func:`jax.lax.pow`: Elementwise power.
    :func:`jax.lax.sqrt`: Elementwise square root.
    :func:`jax.lax.cbrt`: Elementwise cube root.

  .. _stablehlo.rsqrt: https://openxla.org/stablehlo/spec#rsqrt
  """
  return rsqrt_p.bind(x, accuracy=accuracy)

