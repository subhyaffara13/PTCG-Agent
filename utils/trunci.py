
def trunci(out: _ods_ir.Type, in_: _ods_ir.Value, *, overflow_flags: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return TruncIOp(out=out, in_=in_, overflowFlags=overflow_flags, loc=loc, ip=ip).result

