
def binary(sym_name: _Union[str, _ods_ir.StringAttr], objects: _Union[_Any, _ods_ir.ArrayAttr], *, offloading_handler: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> BinaryOp:
  return BinaryOp(sym_name=sym_name, objects=objects, offloadingHandler=offloading_handler, loc=loc, ip=ip)


def binary(output: _ods_ir.Type, x: _ods_ir.Value, y: _ods_ir.Value, *, left_identity: _Optional[bool] = None, right_identity: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BinaryOp(output=output, x=x, y=y, left_identity=left_identity, right_identity=right_identity, loc=loc, ip=ip).result

