
def _dataclass_instance_fields(dcls_instance):
  """Serialization-friendly version of dataclasses.fields for instances."""
  attribute_dict = dcls_instance.__dict__
  fields = []
  for field in dcls_instance.__dataclass_fields__.values():
    if field.name in attribute_dict:  # Filter pseudo-fields.
      fields.append(field)
  return fields

