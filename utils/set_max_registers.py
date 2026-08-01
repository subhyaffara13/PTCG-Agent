
def set_max_registers(n: int, *, action: Literal["increase", "decrease"]):
  """Sets the maximum number of per-lane registers in the thread."""
  set_max_registers_p.bind(n, action=action)

