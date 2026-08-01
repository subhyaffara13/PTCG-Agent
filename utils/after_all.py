
def after_all(inputs: _Sequence[_ods_ir.Value], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AfterAllOp(inputs=inputs, results=results, loc=loc, ip=ip).result


def after_all(inputs: _Sequence[_ods_ir.Value], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AfterAllOp(inputs=inputs, results=results, loc=loc, ip=ip).result


def after_all(*operands):
  """Merges one or more XLA token values. Experimental.

  Wraps the XLA after all operator."""
  operands = core.auto_insert_reshard(*operands)
  return after_all_p.bind(*operands)

