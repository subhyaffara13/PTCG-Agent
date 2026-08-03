from typing import Any

def make_auto_cast_descriptor(
    field: dataclasses.Field[Any], hint: helpers.Hint
) -> helpers.Descriptor:
  """Apply the auto-casting magic to a single class."""
  # TODO(epot): Support `Optional`
  if field.default_factory is not dataclasses.MISSING:
    raise ValueError(
        f'dataclass field {field.name} cannot be both `AutoCast` and'
        ' `default_factory=`'
    )
  # TODO(epot): Propagate other field_kwargs (through likely not necessary)
  return field_utils.field(validate=hint)

