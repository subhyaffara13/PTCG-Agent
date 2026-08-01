
def uitofp(output: _ods_ir.Type, in_: _ods_ir.Value, rounding_mode: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return UIToFPOp(output=output, in_=in_, rounding_mode=rounding_mode, loc=loc, ip=ip).result


def uitofp(out: _ods_ir.Type, in_: _ods_ir.Value, *, non_neg: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return UIToFPOp(out=out, in_=in_, nonNeg=non_neg, loc=loc, ip=ip).result


def uitofp(res: _ods_ir.Type, arg: _ods_ir.Value, *, non_neg: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return UIToFPOp(res=res, arg=arg, nonNeg=non_neg, loc=loc, ip=ip).result

