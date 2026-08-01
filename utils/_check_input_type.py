
def _check_input_type(in_type: core.InputType) -> None:
  # Check that in_type is syntactically well-formed
  assert type(in_type) is tuple
  assert all(isinstance(a, core.AbstractValue) for a in in_type)

