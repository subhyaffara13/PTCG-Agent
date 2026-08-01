
def stmatrix(ptr: _ods_ir.Value, sources: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], layout: _Union[_Any, _ods_ir.Attribute], shape: _Union[_Any, _ods_ir.Attribute], elt_type: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> StMatrixOp:
  return StMatrixOp(ptr=ptr, sources=sources, layout=layout, shape=shape, eltType=elt_type, loc=loc, ip=ip)

