
def element_type_to_backend_config_type_mapping(dtype):
  _element_type_to_backend_config_type_mapping = {
    ir.BF16Type.get(): "BF16",
    ir.F16Type.get(): "F16",
  }
  return _element_type_to_backend_config_type_mapping[dtype]

