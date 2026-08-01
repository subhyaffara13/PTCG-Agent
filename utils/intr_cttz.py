
def intr_cttz(in_: _ods_ir.Value, is_zero_poison: _Union[bool, _ods_ir.BoolAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CountTrailingZerosOp(in_=in_, is_zero_poison=is_zero_poison, results=results, loc=loc, ip=ip).result

