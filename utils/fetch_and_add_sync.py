
def fetch_and_add_sync(base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], value: _ods_ir.Value[_ods_ir.IntegerType], core_id: _ods_ir.Value[_ods_ir.IntegerType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return FetchAndAddSyncOp(base=base, indices=indices, value=value, core_id=core_id, results=results, loc=loc, ip=ip).result

