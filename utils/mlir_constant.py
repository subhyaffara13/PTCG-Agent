
def mlir_constant(value, *, loc=None, ip=None) -> Value:
    return _get_op_result_or_op_results(
        ConstantOp(res=value.type, value=value, loc=loc, ip=ip)
    )


def mlir_constant(res: _ods_ir.Type, value: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConstantOp(res=res, value=value, loc=loc, ip=ip).result

