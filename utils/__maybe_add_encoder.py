
def _MaybeAddEncoder(cls, field_descriptor):
  if hasattr(field_descriptor, '_encoder'):
    return
  is_repeated = field_descriptor.is_repeated
  is_map_entry = _IsMapField(field_descriptor)
  is_packed = field_descriptor.is_packed

  if is_map_entry:
    field_encoder = encoder.MapEncoder(field_descriptor)
    sizer = encoder.MapSizer(field_descriptor,
                             _IsMessageMapField(field_descriptor))
  elif _IsMessageSetExtension(field_descriptor):
    field_encoder = encoder.MessageSetItemEncoder(field_descriptor.number)
    sizer = encoder.MessageSetItemSizer(field_descriptor.number)
  else:
    field_encoder = type_checkers.TYPE_TO_ENCODER[field_descriptor.type](
        field_descriptor.number, is_repeated, is_packed)
    sizer = type_checkers.TYPE_TO_SIZER[field_descriptor.type](
        field_descriptor.number, is_repeated, is_packed)

  field_descriptor._sizer = sizer
  field_descriptor._encoder = field_encoder

