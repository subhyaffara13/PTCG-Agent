
def _is_valid_variables(variables: VariableDict) -> bool:
  """Checks whether the given variable dict is valid.

  Args:
    variables: A variable dict.

  Returns:
    True if `variables` is a valid variable dict.
  """
  for name, col in variables.items():
    if not isinstance(name, str):
      return False
    if not _is_valid_collection(col):
      return False
  return True

