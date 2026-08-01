
def _init_dataclass_state(obj: _Dataclass) -> None:
  """Initialize the object state containing all DataclassField values."""
  if not hasattr(obj, '_dataclass_field_values'):
    # Use object.__setattr__ for frozen dataclasses
    object.__setattr__(obj, '_dataclass_field_values', {})

