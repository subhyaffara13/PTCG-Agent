
def _pspec_mhlo_attrs(spec, aval: core.AbstractValue) -> str:
  if isinstance(aval, core.ShapedArray):
    names = _spec_to_names(spec)
    return str(map(names.get, range(aval.ndim)))
  return ''

