
def make_range(result: _ods_ir.Type, start: _Union[int, _ods_ir.IntegerAttr], end: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return MakeRangeOp(result=result, start=start, end=end, loc=loc, ip=ip).result

