
def _as_hijax_method(name: str) -> tp.Any:
  """Creates a method that operates on the hijax type."""

  def hijax_method_wrapper(hijax_var, *args, **kwargs):
    variable = _get_hijax_state(hijax_var)
    old_state = jax.tree.map(lambda x: x, variable)
    method = getattr(variable, name)
    out = method(*args, **kwargs)
    if _variable_has_changed(old_state, variable):
      _set_hijax_state(hijax_var, variable)
    return out

  hijax_method_wrapper.__name__ = name

  return hijax_method_wrapper

