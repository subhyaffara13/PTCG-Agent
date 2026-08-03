import re

def cast(val, typ):
    log.debug((val, typ))
    if " or " in typ:
        for t in typ.split(" or "):
            try:
                return cast(val, t)
            except TqdmTypeError:
                pass
        raise TqdmTypeError(f"{val} : {typ}")

    # sys.stderr.write('\ndebug | `val:type`: `' + val + ':' + typ + '`.\n')
    if typ == 'bool':
        if (val == 'True') or (val == ''):
            return True
        if val == 'False':
            return False
        raise TqdmTypeError(val + ' : ' + typ)
    if typ == 'chr':
        if len(val) == 1:
            return val.encode()
        if re.match(r"^\\\w+$", val):
            return literal_eval(f'"{val}"').encode()
        raise TqdmTypeError(f"{val} : {typ}")
    if typ == 'str':
        return val
    if typ == 'int':
        try:
            return int(val)
        except ValueError as exc:
            raise TqdmTypeError(f"{val} : {typ}") from exc
    if typ == 'float':
        try:
            return float(val)
        except ValueError as exc:
            raise TqdmTypeError(f"{val} : {typ}") from exc
    raise TqdmTypeError(f"{val} : {typ}")


def cast(typ: type, val: _T) -> _T:  # type: ignore[type-var]
    return val


def cast(dest: _ods_ir.Type, source: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return CastOp(dest=dest, source=source, loc=loc, ip=ip).result

