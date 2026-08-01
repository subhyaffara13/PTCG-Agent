
def _as_hijax_property(name: str, *, get: bool, set: bool) -> property:
  """Creates a property that operates on the hijax type."""

  def _getter_wrapper(hijax_var):
    variable = _get_hijax_state(hijax_var)
    old_state = jax.tree.map(lambda x: x, variable)
    out = getattr(variable, name)
    if _variable_has_changed(old_state, variable):
      _set_hijax_state(hijax_var, variable)
    return out

  def _setter_wrapper(hijax_var, value):
    variable = _get_hijax_state(hijax_var)
    setattr(variable, name, value)
    _set_hijax_state(hijax_var, variable)

  _hijax_property = property(
    fget=_getter_wrapper if get else None,
    fset=_setter_wrapper if set else None,
  )
  return _hijax_property  # type: ignore[return]

