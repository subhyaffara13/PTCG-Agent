
def _aval_to_xla_shape(aval: core.AbstractValue) -> xc.Shape:
  try:
    return _xla_shape_handlers[type(aval)](aval)
  except KeyError as err:
    raise TypeError(f"No xla_shape_handler for type: {type(aval)}") from err

