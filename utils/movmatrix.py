
def movmatrix(src: _ods_ir.Value[_ods_ir.IntegerType], shape: _Union[_Any, _ods_ir.Attribute], elt_type: _Union[_Any, _ods_ir.Attribute], *, layout: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return MovMatrixOp(src=src, shape=shape, eltType=elt_type, layout=layout, results=results, loc=loc, ip=ip).result

