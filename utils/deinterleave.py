
def deinterleave(source: _ods_ir.Value[_ods_ir.VectorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResultList:
  return DeinterleaveOp(source=source, results=results, loc=loc, ip=ip).results

