
def printf(format: _Union[str, _ods_ir.StringAttr], args: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PrintfOp:
  return PrintfOp(format=format, args=args, loc=loc, ip=ip)


def printf(format, *args, loc=None, ip=None):
    return _printf(format=format, args=args, loc=loc, ip=ip)

