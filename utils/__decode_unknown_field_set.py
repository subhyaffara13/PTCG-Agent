
def _DecodeUnknownFieldSet(buffer, pos, end_pos=None, current_depth=0):
  """Decode UnknownFieldSet.  Returns the UnknownFieldSet and new position."""

  unknown_field_set = containers.UnknownFieldSet()
  while end_pos is None or pos < end_pos:
    (tag_bytes, pos) = ReadTag(buffer, pos)
    (tag, _) = _DecodeVarint(tag_bytes, 0)
    field_number, wire_type = wire_format.UnpackTag(tag)
    if wire_type == wire_format.WIRETYPE_END_GROUP:
      break
    (data, pos) = _DecodeUnknownField(
        buffer, pos, end_pos, field_number, wire_type, current_depth
    )
    # pylint: disable=protected-access
    unknown_field_set._add(field_number, wire_type, data)

  return (unknown_field_set, pos)

