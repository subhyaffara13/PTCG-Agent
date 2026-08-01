
def sine(middle: float, pos: float) -> float:
    return (sin((-pi / 2.0) + pi * linear(middle, pos)) + 1.0) / 2.0


def sine(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SineOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result


def sine(operand: _ods_ir.Value[_ods_ir.RankedTensorType], *, result_accuracy: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SineOp(operand=operand, result_accuracy=result_accuracy, results=results, loc=loc, ip=ip).result

