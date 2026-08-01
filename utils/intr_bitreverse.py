
def intr_bitreverse(in_: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BitReverseOp(in_=in_, results=results, loc=loc, ip=ip).result

