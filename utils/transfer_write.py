
def transfer_write(result: _Optional[_ods_ir.Type], value_to_store: _ods_ir.Value[_ods_ir.VectorType], base: _ods_ir.Value, indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], permutation_map: _Union[_ods_ir.AffineMap, _ods_ir.AffineMapAttr], in_bounds: _Union[_Sequence[bool], _ods_ir.ArrayAttr], *, mask: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, TransferWriteOp]:
  op = TransferWriteOp(result=result, valueToStore=value_to_store, base=base, indices=indices, permutation_map=permutation_map, in_bounds=in_bounds, mask=mask, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

