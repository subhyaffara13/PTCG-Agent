
def slice_smem(result: _ods_ir.Type, offset: _Union[int, _ods_ir.IntegerAttr], *, alias_id: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return SliceSMEMOp(result=result, offset=offset, alias_id=alias_id, loc=loc, ip=ip).result

