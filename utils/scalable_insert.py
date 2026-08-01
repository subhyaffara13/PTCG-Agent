
def scalable_insert(value_to_store: _ods_ir.Value[_ods_ir.VectorType], dest: _ods_ir.Value[_ods_ir.VectorType], pos: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ScalableInsertOp(valueToStore=value_to_store, dest=dest, pos=pos, results=results, loc=loc, ip=ip).result

