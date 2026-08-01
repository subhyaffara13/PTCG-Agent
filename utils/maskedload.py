
def maskedload(result: _ods_ir.Type, base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], mask: _ods_ir.Value[_ods_ir.VectorType], pass_thru: _ods_ir.Value[_ods_ir.VectorType], *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MaskedLoadOp(result=result, base=base, indices=indices, mask=mask, pass_thru=pass_thru, alignment=alignment, loc=loc, ip=ip).result

