
def pack_vmsk(output: _ods_ir.Type, sources: _Sequence[_ods_ir.Value[_ods_ir.VectorType]], positions: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return PackMaskOp(output=output, sources=sources, positions=positions, loc=loc, ip=ip).result

