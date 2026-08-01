
def block_id(dimension: _Union[_Any, _ods_ir.Attribute], *, upper_bound: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IndexType]:
  return BlockIdOp(dimension=dimension, upper_bound=upper_bound, results=results, loc=loc, ip=ip).result

