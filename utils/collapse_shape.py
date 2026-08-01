
def collapse_shape(result: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.MemRefType], reassociation: _Union[_Any, _ods_ir.ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return CollapseShapeOp(result=result, src=src, reassociation=reassociation, loc=loc, ip=ip).result

