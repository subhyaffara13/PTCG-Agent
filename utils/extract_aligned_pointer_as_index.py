
def extract_aligned_pointer_as_index(source: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IndexType]:
  return ExtractAlignedPointerAsIndexOp(source=source, results=results, loc=loc, ip=ip).result

