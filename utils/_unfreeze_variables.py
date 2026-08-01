
def _unfreeze_variables(variables, mutable):
  new_variables = {}
  for key, value in variables.items():
    if in_filter(mutable, key):
      new_variables[key] = unfreeze(value)
    else:
      new_variables[key] = value
  return new_variables

