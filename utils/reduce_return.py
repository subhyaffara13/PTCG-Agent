
def reduce_return(result: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ReduceReturnOp:
  return ReduceReturnOp(result=result, loc=loc, ip=ip)


def reduce_return(result: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ReduceReturnOp:
  return ReduceReturnOp(result=result, loc=loc, ip=ip)

