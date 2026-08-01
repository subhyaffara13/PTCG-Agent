
def intr_abs(res: _ods_ir.Type, in_: _ods_ir.Value, is_int_min_poison: _Union[bool, _ods_ir.BoolAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AbsOp(res=res, in_=in_, is_int_min_poison=is_int_min_poison, loc=loc, ip=ip).result

