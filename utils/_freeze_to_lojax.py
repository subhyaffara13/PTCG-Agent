
def _freeze_to_lojax(ref):
  aval = typeof(ref._refs)
  lovals = aval.lower_val(ref._refs)
  vals = [freeze(loval) for loval in lovals]
  return aval.raise_val(*vals)

