
def replicated_to_unreduced(tensor: _ods_ir.Value, axes: _Union[_Any, _ods_ir.Attribute], out_sharding: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ReplicatedToUnreducedOp(tensor=tensor, axes=axes, out_sharding=out_sharding, results=results, loc=loc, ip=ip).result

