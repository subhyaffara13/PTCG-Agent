
def transfer_read(vector: _ods_ir.Type, base: _ods_ir.Value, indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], permutation_map: _Union[_ods_ir.AffineMap, _ods_ir.AffineMapAttr], padding: _ods_ir.Value, in_bounds: _Union[_Sequence[bool], _ods_ir.ArrayAttr], *, mask: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return TransferReadOp(vector=vector, base=base, indices=indices, permutation_map=permutation_map, padding=padding, in_bounds=in_bounds, mask=mask, loc=loc, ip=ip).result

