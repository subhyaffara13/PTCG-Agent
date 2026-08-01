
def atomic_cas(result: _ods_ir.Type, ptr: _ods_ir.Value, cmp: _ods_ir.Value, val: _ods_ir.Value, sem: _Union[_Any, _ods_ir.Attribute], scope: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AtomicCASOp(result=result, ptr=ptr, cmp=cmp, val=val, sem=sem, scope=scope, loc=loc, ip=ip).result


def atomic_cas(ref, cmp, val):
  """Performs an atomic compare-and-swap of the value in the ref with the

  given value.

  Args:
    ref: The ref to operate on.
    cmp: The expected value to compare against.
    val: The value to swap in.

  Returns:
    The value at the given index prior to the atomic operation.
  """
  return atomic_cas_p.bind(ref, cmp, val)

