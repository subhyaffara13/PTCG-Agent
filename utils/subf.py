
def subf(pattern, format, string, count=0, flags=0, pos=None, endpos=None,
  concurrent=None, timeout=None, ignore_unused=False, **kwargs):
    """Return the string obtained by replacing the leftmost (or rightmost with a
    reverse pattern) non-overlapping occurrences of the pattern in string by the
    replacement format. format can be either a string or a callable; if a string,
    it's treated as a format string; if a callable, it's passed the match object
    and must return a replacement string to be used."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.subf(format, string, count, pos, endpos, concurrent, timeout)


def subf(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, roundingmode: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubFOp(lhs=lhs, rhs=rhs, fastmath=fastmath, roundingmode=roundingmode, results=results, loc=loc, ip=ip).result


def subf(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, rnd: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, sat: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return SubFOp(lhs=lhs, rhs=rhs, rnd=rnd, sat=sat, ftz=ftz, results=results, loc=loc, ip=ip).result


def subf(a: ir.Value, b: ir.Value):
  return arith.subf(a, b, fastmath=arith.FastMathFlags.contract)

