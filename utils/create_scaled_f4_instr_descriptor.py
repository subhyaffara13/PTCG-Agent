
def create_scaled_f4_instr_descriptor(*args, **kwargs) -> ir.Value:
  def get_input_encoding(ty):
    if ty == ir.Float4E2M1FNType.get():
      return 1
    else:
      raise NotImplementedError(f"Unsupported input dtype: {ty}")
  return _create_scaled_instr_descriptor(get_input_encoding, *args, **kwargs)

