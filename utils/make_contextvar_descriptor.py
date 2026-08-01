
def make_contextvar_descriptor(
    field: dataclasses.Field[Any], hint: helpers.Hint
) -> _ContextvarDescriptor:
  """Replace `ContextVar[]` annotated fields with contextvar descriptor."""
  del hint
  return _ContextvarDescriptor(field)

