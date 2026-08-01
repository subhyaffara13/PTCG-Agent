
def _MaybeAddDecoder(cls, field_descriptor):
  if hasattr(field_descriptor, '_decoders'):
    return

  is_repeated = field_descriptor.is_repeated
  is_map_entry = _IsMapField(field_descriptor)
  helper_decoders = {}

  def AddDecoder(is_packed):
    decode_type = field_descriptor.type
    if (decode_type == _FieldDescriptor.TYPE_ENUM and
        not field_descriptor.enum_type.is_closed):
      decode_type = _FieldDescriptor.TYPE_INT32

    oneof_descriptor = None
    if field_descriptor.containing_oneof is not None:
      oneof_descriptor = field_descriptor

    if is_map_entry:
      is_message_map = _IsMessageMapField(field_descriptor)

      field_decoder = decoder.MapDecoder(
          field_descriptor, _GetInitializeDefaultForMap(field_descriptor),
          is_message_map)
    elif decode_type == _FieldDescriptor.TYPE_STRING:
      field_decoder = decoder.StringDecoder(
          field_descriptor.number, is_repeated, is_packed,
          field_descriptor, field_descriptor._default_constructor,
          not field_descriptor.has_presence)
    elif field_descriptor.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
      field_decoder = type_checkers.TYPE_TO_DECODER[decode_type](
          field_descriptor.number, is_repeated, is_packed,
          field_descriptor, field_descriptor._default_constructor)
    else:
      field_decoder = type_checkers.TYPE_TO_DECODER[decode_type](
          field_descriptor.number, is_repeated, is_packed,
          # pylint: disable=protected-access
          field_descriptor, field_descriptor._default_constructor,
          not field_descriptor.has_presence)

    helper_decoders[is_packed] = field_decoder

  AddDecoder(False)

  if is_repeated and wire_format.IsTypePackable(field_descriptor.type):
    # To support wire compatibility of adding packed = true, add a decoder for
    # packed values regardless of the field's options.
    AddDecoder(True)

  field_descriptor._decoders = helper_decoders

