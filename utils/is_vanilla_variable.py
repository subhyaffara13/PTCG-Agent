
def is_vanilla_variable(vs: variablelib.Variable) -> bool:
  """A variable is vanilla if its metadata is essentially blank.

  Returns False only if it has non-empty hooks or any non-built-in attribute.
  """
  for key, value in vs.get_metadata().items():
    if key in variablelib.Variable.required_metadata:
      continue
    if key.endswith('_hooks') and value == ():
      continue
    return False
  return True

