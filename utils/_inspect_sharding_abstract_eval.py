
def _inspect_sharding_abstract_eval(aval, **_):
  del aval
  # Effectful abstract avoids DCE
  return [], {debug_effect}

