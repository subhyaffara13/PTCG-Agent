
def reduce_precision(operand: _ods_ir.Value[_ods_ir.RankedTensorType], exponent_bits: _Union[int, _ods_ir.IntegerAttr], mantissa_bits: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReducePrecisionOp(operand=operand, exponent_bits=exponent_bits, mantissa_bits=mantissa_bits, results=results, loc=loc, ip=ip).result


def reduce_precision(operand: _ods_ir.Value[_ods_ir.RankedTensorType], exponent_bits: _Union[int, _ods_ir.IntegerAttr], mantissa_bits: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReducePrecisionOp(operand=operand, exponent_bits=exponent_bits, mantissa_bits=mantissa_bits, results=results, loc=loc, ip=ip).result


def reduce_precision(x):
  if (h := reduce_precision_handlers.get(type(t := core.typeof(x)))):
    return h(t, x)
  return x


def reduce_precision(operand: float | ArrayLike,
                     exponent_bits: int,
                     mantissa_bits: int) -> Array:
  """Wraps XLA's `ReducePrecision
  <https://www.openxla.org/xla/operation_semantics#reduceprecision>`_
  operator.
  """
  exponent_bits = core.concrete_or_error(
    operator.index, exponent_bits, "exponent_bits argument of lax.reduce_precision")
  mantissa_bits = core.concrete_or_error(
    operator.index, mantissa_bits, "mantissa_bits argument of lax.reduce_precision")
  return reduce_precision_p.bind(operand, exponent_bits=exponent_bits,
                                 mantissa_bits=mantissa_bits)

