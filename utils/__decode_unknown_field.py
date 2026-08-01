
def _DecodeUnknownField(
    buffer, pos, end_pos, field_number, wire_type, current_depth=0
):
  """Decode a unknown field.  Returns the UnknownField and new position."""

  if wire_type == wire_format.WIRETYPE_VARINT:
    (data, pos) = _DecodeVarint(buffer, pos)
  elif wire_type == wire_format.WIRETYPE_FIXED64:
    (data, pos) = _DecodeFixed64(buffer, pos)
  elif wire_type == wire_format.WIRETYPE_FIXED32:
    (data, pos) = _DecodeFixed32(buffer, pos)
  elif wire_type == wire_format.WIRETYPE_LENGTH_DELIMITED:
    (size, pos) = _DecodeVarint(buffer, pos)
    data = buffer[pos:pos+size].tobytes()
    pos += size
  elif wire_type == wire_format.WIRETYPE_START_GROUP:
    end_tag_bytes = encoder.TagBytes(
        field_number, wire_format.WIRETYPE_END_GROUP
    )
    current_depth += 1
    if current_depth >= _recursion_limit:
      raise _DecodeError('Error parsing message: too many levels of nesting.')
    data, pos = _DecodeUnknownFieldSet(buffer, pos, end_pos, current_depth)
    current_depth -= 1
    # Check end tag.
    if buffer[pos - len(end_tag_bytes) : pos] != end_tag_bytes:
      raise _DecodeError('Missing group end tag.')
  elif wire_type == wire_format.WIRETYPE_END_GROUP:
    return (0, -1)
  else:
    raise _DecodeError('Wrong wire type in tag.')

  if pos > end_pos:
    raise _DecodeError('Truncated message.')

  return (data, pos)

