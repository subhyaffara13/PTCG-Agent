
def mlir_global_dtors(dtors: _Union[_Sequence[str], _ods_ir.ArrayAttr], priorities: _Union[_Sequence[int], _ods_ir.ArrayAttr], data: _Union[_Sequence[_ods_ir.Attribute], _ods_ir.ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> GlobalDtorsOp:
  return GlobalDtorsOp(dtors=dtors, priorities=priorities, data=data, loc=loc, ip=ip)

