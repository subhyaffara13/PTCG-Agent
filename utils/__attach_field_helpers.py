
def _AttachFieldHelpers(cls, field_descriptor):
  field_descriptor._default_constructor = _DefaultValueConstructorForField(
      field_descriptor
  )

  def AddFieldByTag(wiretype, is_packed):
    tag_bytes = encoder.TagBytes(field_descriptor.number, wiretype)
    cls._fields_by_tag[tag_bytes] = (field_descriptor, is_packed)

  AddFieldByTag(
      type_checkers.FIELD_TYPE_TO_WIRE_TYPE[field_descriptor.type], False
  )

  if field_descriptor.is_repeated and wire_format.IsTypePackable(
      field_descriptor.type
  ):
    # To support wire compatibility of adding packed = true, add a decoder for
    # packed values regardless of the field's options.
    AddFieldByTag(wire_format.WIRETYPE_LENGTH_DELIMITED, True)

