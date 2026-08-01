
def MessageDecoder(field_number, is_repeated, is_packed, key, new_default):
  """Returns a decoder for a message field."""

  local_DecodeVarint = _DecodeVarint

  assert not is_packed
  if is_repeated:
    tag_bytes = encoder.TagBytes(field_number,
                                 wire_format.WIRETYPE_LENGTH_DELIMITED)
    tag_len = len(tag_bytes)
    def DecodeRepeatedField(
        buffer, pos, end, message, field_dict, current_depth=0
    ):
      value = field_dict.get(key)
      if value is None:
        value = field_dict.setdefault(key, new_default(message))
      while 1:
        # Read length.
        (size, pos) = local_DecodeVarint(buffer, pos)
        new_pos = pos + size
        if new_pos > end:
          raise _DecodeError('Truncated message.')
        # Read sub-message.
        current_depth += 1
        if current_depth > _recursion_limit:
          raise _DecodeError(
              'Error parsing message: too many levels of nesting.'
          )
        if (
            value.add()._InternalParse(buffer, pos, new_pos, current_depth)
            != new_pos
        ):
          # The only reason _InternalParse would return early is if it
          # encountered an end-group tag.
          raise _DecodeError('Unexpected end-group tag.')
        current_depth -= 1
        # Predict that the next tag is another copy of the same repeated field.
        pos = new_pos + tag_len
        if buffer[new_pos:pos] != tag_bytes or new_pos == end:
          # Prediction failed.  Return.
          return new_pos

    return DecodeRepeatedField
  else:

    def DecodeField(buffer, pos, end, message, field_dict, current_depth=0):
      value = field_dict.get(key)
      if value is None:
        value = field_dict.setdefault(key, new_default(message))
      # Read length.
      (size, pos) = local_DecodeVarint(buffer, pos)
      new_pos = pos + size
      if new_pos > end:
        raise _DecodeError('Truncated message.')
      # Read sub-message.
      current_depth += 1
      if current_depth > _recursion_limit:
        raise _DecodeError('Error parsing message: too many levels of nesting.')
      if value._InternalParse(buffer, pos, new_pos, current_depth) != new_pos:
        # The only reason _InternalParse would return early is if it encountered
        # an end-group tag.
        raise _DecodeError('Unexpected end-group tag.')
      current_depth -= 1
      return new_pos

    return DecodeField

