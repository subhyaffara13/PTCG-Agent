
def _set_shaped_array_attributes(shaped_array):
  # Set up operator, method, and property forwarding on Tracer instances
  # containing
  # ShapedArray avals by following the forwarding conventions for Tracer.
  # Forward operators using a single-underscore-prefix naming convention:
  for operator_name, function in _array_operators.items():
    setattr(shaped_array, f"_{operator_name}", staticmethod(function))
  # Forward methods and properties using core.{aval_method, aval_property}:
  for method_name, method in _array_methods.items():
    setattr(shaped_array, method_name, core.aval_method(method))
  for prop_name, prop in _array_properties.items():
    setattr(shaped_array, prop_name, core.aval_property(prop))
  setattr(shaped_array, "_array_module", staticmethod(__array_module__))

