
def reinterpret_cast(
    result,
    input,
    dynamic_sizes=None,
    *,
    dynamic_offset=None,
    loc=None,
    ip=None,
):
  if dynamic_sizes is None:
    dynamic_sizes = []
  return _tpu_ops_gen.ReinterpretCastOp(
      result,
      input,
      dynamic_offset=dynamic_offset,
      dynamic_sizes=dynamic_sizes,
      loc=loc,
      ip=ip,
  ).result


def reinterpret_cast(result: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.MemRefType], dynamic_sizes: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, dynamic_offset: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return ReinterpretCastOp(result=result, input=input, dynamic_sizes=dynamic_sizes, dynamic_offset=dynamic_offset, loc=loc, ip=ip).result


def reinterpret_cast(result: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return ReinterpretCastOp(result=result, source=source, loc=loc, ip=ip).result


def reinterpret_cast(result: _ods_ir.Type, source: _ods_ir.Value, offsets: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], sizes: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], strides: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], static_offsets: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], static_sizes: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], static_strides: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return ReinterpretCastOp(result=result, source=source, offsets=offsets, sizes=sizes, strides=strides, static_offsets=static_offsets, static_sizes=static_sizes, static_strides=static_strides, loc=loc, ip=ip).result

