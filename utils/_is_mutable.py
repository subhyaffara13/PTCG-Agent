
def _is_mutable(axis_col: str) -> bool:
  """Determines whether a collection is mutable.

  For example, when a module is called with `module.apply(..., mutable=['z'])`,
  this function will return True for `axis_col='z'` and False otherwise.

  If there is no module in scope, this function will return True.

  Args:
    axis_col: Name of the collection in question.

  Returns:
    Whether it is currently mutable.
  """
  last = nn.module._context.module_stack[-1]  # pylint: disable=protected-access
  if last:
    return last.is_mutable_collection(axis_col)
  else:
    return True

