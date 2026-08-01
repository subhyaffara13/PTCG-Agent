
def _set_tracer_aval_forwarding(tracer, exclude=()):
  for operator_name in _array_operators:
    if operator_name not in exclude:
      setattr(tracer, f"__{operator_name}__", _forward_operator_to_aval(operator_name))
  for method_name in _array_methods:
    if method_name not in exclude:
      setattr(tracer, method_name, _forward_method_to_aval(method_name))
  for prop_name in _array_properties:
    if prop_name not in exclude:
      setattr(tracer, prop_name, _forward_property_to_aval(prop_name))

