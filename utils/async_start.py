
def async_start(result: _ods_ir.Type, inputs: _Sequence[_ods_ir.Value], called_computation: _Union[str, _ods_ir.FlatSymbolRefAttr], execution_thread: _Union[str, _ods_ir.StringAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AsyncStartOp(result=result, inputs=inputs, called_computation=called_computation, execution_thread=execution_thread, loc=loc, ip=ip).result


def async_start(result: _ods_ir.Type, operands_: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AsyncStartOp(result=result, operands_=operands_, loc=loc, ip=ip).result

