
def _is_valid_collection(col: VariableDict):
  if not isinstance(col, (FrozenDict, dict)):
    return False
  for name in col.keys():
    # Any value can be stored in a collection so only keys can be verified.
    if not isinstance(name, str):
      return False
  return True

