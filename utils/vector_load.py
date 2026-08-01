
def vector_load(
    result,
    base,
    indices,
    *,
    strides=None,
    mask=None,
    loc=None,
    ip=None,
):
  if strides is None:
    strides = []
  return VectorLoadOp(
      result, base, indices, strides, mask=mask, loc=loc, ip=ip
  ).result


def vector_load(result: _ods_ir.Type, base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], strides: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, mask: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return VectorLoadOp(result=result, base=base, indices=indices, strides=strides, mask=mask, loc=loc, ip=ip).result


def vector_load(source: _ods_ir.Value[_ods_ir.MemRefType], *, optimized: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return VectorLoadOp(source=source, optimized=optimized, results=results, loc=loc, ip=ip).result

