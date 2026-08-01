
def dataclass_from_attributes(cls: type[T], **field_values) -> T:
  """Directly instantiates a dataclass given all of its fields.

  Dataclasses can override ``__init__`` to have arbitrary custom behavior, but
  this may make it difficult to construct new instances of dataclasses with
  particular field values. This function makes it possible to directly
  instantiate an instance of a dataclass with given attributes.

  Callers of this method are responsible for maintaining any invariants
  expected by the class. The intended use of this function is to restore a
  dataclass from field values extracted from another instance of that exact
  dataclass type.

  Args:
    cls: Class to instantiate.
    **field_values: Values for each of the dataclass's fields

  Returns:
    A new instance of the class.
  """
  # Make sure our fields are correct.
  expected_fields = dataclasses.fields(cls)
  expected_names = set(field.name for field in expected_fields)
  given_names = set(field_values.keys())
  if expected_names != given_names:
    raise ValueError(
        "Incorrect fields provided to `dataclass_from_attributes`; expected"
        f" {expected_names}, got {given_names}"
    )
  # Make a new object, bypassing the class's initializer.
  value = object.__new__(cls)
  # Set all the attributes, bypassing the class's __setattr__.
  for k, v in field_values.items():
    object.__setattr__(value, k, v)
  return value

