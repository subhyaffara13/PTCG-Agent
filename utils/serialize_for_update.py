
def serialize_for_update(**kwargs) -> SerializedMetadata:
  """Validates and serializes `kwargs` to a dictionary.

  To be used with MetadataStore.update().

  Args:
    **kwargs: The kwargs to be serialized.

  Returns:
    A dictionary of the serialized kwargs.
  """
  fields = dataclasses.fields(InternalCheckpointMetadata)
  field_names = {field.name for field in fields}

  for k in kwargs:
    if k not in field_names:
      raise ValueError('Provided metadata contains unknown key %s.' % k)

  validated_kwargs = {
      field.name: field.metadata['processor'](kwargs[field.name])
      for field in fields
      if field.name in kwargs
  }

  return validated_kwargs

