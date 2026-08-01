
def shuffled_store(value_to_store: _ods_ir.Value[_ods_ir.VectorType], base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], sublane_mask: _Union[_Sequence[bool], _ods_ir.DenseBoolArrayAttr], sublane_offsets: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ShuffledStoreOp:
  return ShuffledStoreOp(valueToStore=value_to_store, base=base, indices=indices, sublane_mask=sublane_mask, sublane_offsets=sublane_offsets, loc=loc, ip=ip)

