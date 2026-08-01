
def get_ref_aval_from_value(x: Any):
  if type(x) in _ref_type_aval_mappings:
    return _ref_type_aval_mappings[type(x)](x)
  return _default_value_to_ref_aval(x)

