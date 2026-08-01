
def dim(t: str) -> str:
    return _c(_DIM, t)


def dim(g: jit_utils.GraphContext, self):
    """Implement the dim functionality available for a pytorch tensor in ONNX"""
    # ONNX does not support dim directly in this opset so we can use 2 ops to get the info
    shape = g.op("Shape", self)
    return g.op("Size", shape)


def dim(source: _ods_ir.Value, index: _ods_ir.Value[_ods_ir.IndexType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IndexType]:
  return DimOp(source=source, index=index, results=results, loc=loc, ip=ip).result

