
def _select_weak_type_rule(which, *cases):
  return all(c.weak_type for c in cases)

