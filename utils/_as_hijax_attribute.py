
def _as_hijax_attribute(name: str) -> property:
  """Creates a property that operates on the hijax type."""

  def _getter_wrapper(hijax_var):
    variable = _get_hijax_state(hijax_var)
    old_state = jax.tree.map(lambda x: x, variable)
    out = getattr(variable, name)
    if _variable_has_changed(old_state, variable):
      _set_hijax_state(hijax_var, variable)
    return out

  _getter_wrapper.__name__ = name
  _hijax_property = property(fget=_getter_wrapper)

  return _hijax_property  # type: ignore[return]

