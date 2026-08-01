
def vector_store(
    value_to_store,
    base,
    indices,
    *,
    strides=None,
    add=False,
    mask=None,
    loc=None,
    ip=None,
):
  if strides is None:
    strides = []
  return VectorStoreOp(
      value_to_store, base, indices, strides, mask=mask, add=add, loc=loc, ip=ip
  )


def vector_store(value_to_store: _ods_ir.Value[_ods_ir.VectorType], base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], strides: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, mask: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, add: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> VectorStoreOp:
  return VectorStoreOp(valueToStore=value_to_store, base=base, indices=indices, strides=strides, mask=mask, add=add, loc=loc, ip=ip)


def vector_store(value_to_store: _ods_ir.Value[_ods_ir.VectorType], destination: _ods_ir.Value[_ods_ir.MemRefType], *, optimized: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, atomic_type: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, multimem: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> VectorStoreOp:
  return VectorStoreOp(valueToStore=value_to_store, destination=destination, optimized=optimized, atomic_type=atomic_type, multimem=multimem, loc=loc, ip=ip)

