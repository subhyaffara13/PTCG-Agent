
def check_layout_assignment(var: cs.Variable, layout: cs.Constant) -> None:
  """Raises if the given layout can not be assigned to the given `Variable`."""
  if not cs.is_valid_assignment(var, layout):
    raise ValueError(
        f"Variable {var} in memory space {var.memory_space} should not be "
        f"assigned a layout of type {type(layout)}. This is a bug."
    )

