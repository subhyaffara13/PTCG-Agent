
def MessageSetItemDecoder(descriptor):
  """Returns a decoder for a MessageSet item.

  The parameter is the message Descriptor.

  The message set message looks like this:
    message MessageSet {
      repeated group Item = 1 {
        required int32 type_id = 2;
        required string message = 3;
      }
    }
  """

  type_id_tag_bytes = encoder.TagBytes(2, wire_format.WIRETYPE_VARINT)
  message_tag_bytes = encoder.TagBytes(3, wire_format.WIRETYPE_LENGTH_DELIMITED)
  item_end_tag_bytes = encoder.TagBytes(1, wire_format.WIRETYPE_END_GROUP)

  local_ReadTag = ReadTag
  local_DecodeVarint = _DecodeVarint

  def DecodeItem(buffer, pos, end, message, field_dict, current_depth=0):
    """Decode serialized message set to its value and new position.

    Args:
      buffer: memoryview of the serialized bytes.
      pos: int, position in the memory view to start at.
      end: int, end position of serialized data
      message: Message object to store unknown fields in
      field_dict: Map[Descriptor, Any] to store decoded values in.

    Returns:
      int, new position in serialized data.
    """
    message_set_item_start = pos
    type_id = -1
    message_start = -1
    message_end = -1

    # Technically, type_id and message can appear in any order, so we need
    # a little loop here.
    while 1:
      (tag_bytes, pos) = local_ReadTag(buffer, pos)
      if tag_bytes == type_id_tag_bytes:
        (type_id, pos) = local_DecodeVarint(buffer, pos)
      elif tag_bytes == message_tag_bytes:
        (size, message_start) = local_DecodeVarint(buffer, pos)
        pos = message_end = message_start + size
      elif tag_bytes == item_end_tag_bytes:
        break
      else:
        field_number, wire_type = DecodeTag(tag_bytes)
        _, pos = _DecodeUnknownField(buffer, pos, end, field_number, wire_type)
        if pos == -1:
          raise _DecodeError('Unexpected end-group tag.')

    if pos > end:
      raise _DecodeError('Truncated message.')

    if type_id == -1:
      raise _DecodeError('MessageSet item missing type_id.')
    if message_start == -1:
      raise _DecodeError('MessageSet item missing message.')

    extension = message.Extensions._FindExtensionByNumber(type_id)
    # pylint: disable=protected-access
    if extension is not None:
      value = field_dict.get(extension)
      if value is None:
        message_type = extension.message_type
        if not hasattr(message_type, '_concrete_class'):
          message_factory.GetMessageClass(message_type)
        value = field_dict.setdefault(
            extension, message_type._concrete_class())
      current_depth += 1
      if current_depth > _recursion_limit:
        raise _DecodeError('Error parsing message: too many levels of nesting.')
      if (
          value._InternalParse(
              buffer, message_start, message_end, current_depth
          )
          != message_end
      ):
        # The only reason _InternalParse would return early is if it encountered
        # an end-group tag.
        raise _DecodeError('Unexpected end-group tag.')
      current_depth -= 1
    else:
      if not message._unknown_fields:
        message._unknown_fields = []
      message._unknown_fields.append(
          (MESSAGE_SET_ITEM_TAG, buffer[message_set_item_start:pos].tobytes()))
      # pylint: enable=protected-access

    return pos

  return DecodeItem

