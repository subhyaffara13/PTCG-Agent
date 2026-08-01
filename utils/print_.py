
def print_(prefix: _Union[str, _ods_ir.StringAttr], hex: _Union[bool, _ods_ir.BoolAttr], args: _Sequence[_ods_ir.Value], is_signed: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PrintOp:
  return PrintOp(prefix=prefix, hex=hex, args=args, isSigned=is_signed, loc=loc, ip=ip)


def print_(tensor: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PrintOp:
  return PrintOp(tensor=tensor, loc=loc, ip=ip)


def print_(*, source: _Optional[_ods_ir.Value] = None, punctuation: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, string_literal: _Optional[_Union[_Any, _ods_ir.StringAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PrintOp:
  return PrintOp(source=source, punctuation=punctuation, stringLiteral=string_literal, loc=loc, ip=ip)

