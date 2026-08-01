
def _pad_ur_rule(operand, padding_value, *, padding_config):
  return core.getu(operand), core.getr(operand)

