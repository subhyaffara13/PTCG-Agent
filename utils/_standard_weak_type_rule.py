
def _standard_weak_type_rule(*avals, **kwargs):
  return all(aval.weak_type for aval in avals)

