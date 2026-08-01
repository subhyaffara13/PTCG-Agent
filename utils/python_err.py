
def python_err(err_tree, *args):
  error = tree_unflatten(err_tree, args)
  _check_error(error)
  return []

