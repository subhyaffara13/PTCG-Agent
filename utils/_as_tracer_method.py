
def _as_tracer_method(name: str):
  def op(self, hijax_var, *args, **kwargs):
    variable = _get_hijax_state(hijax_var)
    old_state = jax.tree.map(lambda x: x, variable)
    out = getattr(variable, name)(*args, **kwargs)
    if _variable_has_changed(old_state, variable):
      _set_hijax_state(hijax_var, variable)
    return out

  op.__name__ = name
  return op

