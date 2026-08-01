
def _set_array_abstract_methods(basearray):
  for operator_name, function in _array_operators.items():
    setattr(basearray, f"__{operator_name}__",
            _make_abstract_method(f"__{operator_name}__", function))
  for method_name, method in _array_methods.items():
    setattr(basearray, method_name,
            _make_abstract_method(method_name, method))
  for prop_name, prop in _array_properties.items():
    setattr(basearray, prop_name,
            property(_make_abstract_method(prop_name, prop)))

