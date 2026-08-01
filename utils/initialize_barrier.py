
def initialize_barrier(base_pointer: _ods_ir.Value, arrival_count: _Union[int, _ods_ir.IntegerAttr], num_barriers: _Union[int, _ods_ir.IntegerAttr], orders_tensor_core: _Union[bool, _ods_ir.BoolAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> InitializeBarrierOp:
  return InitializeBarrierOp(base_pointer=base_pointer, arrival_count=arrival_count, num_barriers=num_barriers, orders_tensor_core=orders_tensor_core, loc=loc, ip=ip)

