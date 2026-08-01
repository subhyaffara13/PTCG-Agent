
def lvl(source: _ods_ir.Value[_ods_ir.RankedTensorType], index: _ods_ir.Value[_ods_ir.IndexType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IndexType]:
  return LvlOp(source=source, index=index, results=results, loc=loc, ip=ip).result

