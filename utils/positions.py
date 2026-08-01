
def positions(tensor: _ods_ir.Value[_ods_ir.RankedTensorType], level: _Union[_Any, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return ToPositionsOp(tensor=tensor, level=level, results=results, loc=loc, ip=ip).result

