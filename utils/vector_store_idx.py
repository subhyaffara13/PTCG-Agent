
def vector_store_idx(value_to_store: _ods_ir.Value[_ods_ir.VectorType], base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.VectorType]], *, mask: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, add: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> VectorStoreIdxOp:
  return VectorStoreIdxOp(valueToStore=value_to_store, base=base, indices=indices, mask=mask, add=add, loc=loc, ip=ip)

