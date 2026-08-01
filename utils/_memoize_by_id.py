
def _memoize_by_id(fn, refs):
  """Memoization by module/variable id to handle aliasing in traversal."""

  @functools.wraps(fn)
  def wrapped_fn(x):
    nonlocal refs
    if isinstance(x, (VariablePlaceholder, InstancePlaceholder)):
      x_id = x.id
    elif isinstance(x, (Variable, Module)):
      x_id = x._id
    else:
      return fn(x)
    if x_id not in refs:
      refs[x_id] = fn(x)
    return refs[x_id]

  return wrapped_fn

