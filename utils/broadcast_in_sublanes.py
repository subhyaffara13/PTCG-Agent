
def broadcast_in_sublanes(output: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], lane: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return BroadcastInSublanesOp(output=output, source=source, lane=lane, loc=loc, ip=ip).result

