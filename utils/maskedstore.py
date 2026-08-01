
def maskedstore(base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], mask: _ods_ir.Value[_ods_ir.VectorType], value_to_store: _ods_ir.Value[_ods_ir.VectorType], *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MaskedStoreOp:
  return MaskedStoreOp(base=base, indices=indices, mask=mask, valueToStore=value_to_store, alignment=alignment, loc=loc, ip=ip)

