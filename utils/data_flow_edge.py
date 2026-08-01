
def data_flow_edge(input: _ods_ir.Value, *, sharding: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DataFlowEdgeOp(input=input, sharding=sharding, results=results, loc=loc, ip=ip).result

