
def ldmatrix(res: _ods_ir.Type, src_memref: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], transpose: _Union[bool, _ods_ir.BoolAttr], num_tiles: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return LdMatrixOp(res=res, srcMemref=src_memref, indices=indices, transpose=transpose, numTiles=num_tiles, loc=loc, ip=ip).result


def ldmatrix(ptr: _ods_ir.Value, num: _Union[int, _ods_ir.IntegerAttr], layout: _Union[_Any, _ods_ir.Attribute], shape: _Union[_Any, _ods_ir.Attribute], elt_type: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LdMatrixOp(ptr=ptr, num=num, layout=layout, shape=shape, eltType=elt_type, results=results, loc=loc, ip=ip).result

