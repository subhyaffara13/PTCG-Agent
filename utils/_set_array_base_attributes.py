
def _set_array_base_attributes(array_impl, include=None, exclude=None):
  # Forward operators, methods, and properties on Array to lax_numpy
  # functions (with no Tracers involved; this forwarding is direct)
  def maybe_setattr(attr_name, target):
    if exclude is not None and attr_name in exclude:
      return
    if not include or attr_name in include:
      setattr(array_impl, attr_name, target)

  for operator_name, function in _array_operators.items():
    maybe_setattr(f"__{operator_name}__", function)
  for method_name, method in _array_methods.items():
    maybe_setattr(method_name, method)
  for prop_name, prop in _array_properties.items():
    maybe_setattr(prop_name, property(prop))

  for name, func in _impl_only_array_methods.items():
    setattr(array_impl, name, func)

