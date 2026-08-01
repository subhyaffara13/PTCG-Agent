
def create_scaled_f8f6f4_instr_descriptor(*args, **kwargs) -> ir.Value:
  def get_input_encoding(ty):
    if ty == ir.Float8E4M3FNType.get():
      return 0
    elif ty == ir.Float8E5M2Type.get():
      return 1
    else:
      raise NotImplementedError(f"Unsupported input dtype: {ty}")
  return _create_scaled_instr_descriptor(get_input_encoding, *args, **kwargs)

