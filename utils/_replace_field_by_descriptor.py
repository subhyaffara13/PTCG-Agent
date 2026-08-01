
def _replace_field_by_descriptor(
    cls: _Cls,
    *,
    descriptor_infos: list[DescriptorInfo],
):
  """Iterate over the dataclass fields and replace the fields by descriptors."""
  if not dataclasses.is_dataclass(cls):  # e.g. object
    return
  fields = {f.name: f for f in dataclasses.fields(cls)}
  hints = _get_type_hints(cls, include_extras=True)

  for name, hint in hints.items():
    if name not in cls.__annotations__:
      continue  # Only add typing from the current class
    # TODO(epot): Should create a typing parsing util.
    if typing_extensions.get_origin(hint) is not Annotated:
      continue

    hint_cls = hint.__origin__  # Unwrap the original type
    field = fields[name]

    # Make the descriptor
    for descriptor_info in descriptor_infos:
      if not any(
          a is descriptor_info.annotated_token for a in hint.__metadata__
      ):
        continue
      descriptor = descriptor_info.descriptor_fn(field, hint_cls)
      setattr(cls, name, descriptor)  # cls.__dict__[name] = cast_field
      descriptor.__set_name__(cls, name)  # Notify the descriptor

