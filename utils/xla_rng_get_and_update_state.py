
def xla_rng_get_and_update_state(delta: _Union[int, _ods_ir.IntegerAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return XlaRngGetAndUpdateStateOp(delta=delta, results=results, loc=loc, ip=ip).result

