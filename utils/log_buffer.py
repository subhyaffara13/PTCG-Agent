
def log_buffer(input: _ods_ir.Value[_ods_ir.MemRefType], shape: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], tag: _Union[str, _ods_ir.StringAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> LogBufferOp:
  return LogBufferOp(input=input, shape=shape, tag=tag, loc=loc, ip=ip)

