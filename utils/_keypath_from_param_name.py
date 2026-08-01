
def _keypath_from_param_name(param_name: str) -> tree_types.PyTreeKeyPath:
  """Converts a param name to a PyTreeKeyPath.

  This is based on reversing the name construction from `tree/utils.py`'s
  `param_name_from_keypath`.

  Args:
    param_name: A string representing the parameter name.

  Returns:
    A PyTreeKeyPath representing the parameter name.
  """
  if not param_name:
    return ()
  return tuple([jtu.GetAttrKey(s) for s in param_name.split('.')])

