
def zext(res: _ods_ir.Type, arg: _ods_ir.Value, *, non_neg: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ZExtOp(res=res, arg=arg, nonNeg=non_neg, loc=loc, ip=ip).result

