
def _update_annotation(
    f: lu.WrappedFun,
    orig_type: tuple[core.AbstractValue, ...] | None,
    nonzeros: list[bool]
  ) -> lu.WrappedFun:
  if orig_type is None:
    return f
  tan_types = [aval.to_tangent_aval() for nz, aval in zip(nonzeros, orig_type) if nz]
  return lu.annotate(f, (*orig_type, *tan_types))

