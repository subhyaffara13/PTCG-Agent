
def _AddMergeFromStringMethod(message_descriptor, cls):
  """Helper for _AddMessageMethods()."""
  def MergeFromString(self, serialized):
    serialized = memoryview(serialized)
    length = len(serialized)
    try:
      if self._InternalParse(serialized, 0, length) != length:
        # The only reason _InternalParse would return early is if it
        # encountered an end-group tag.
        raise message_mod.DecodeError('Unexpected end-group tag.')
    except (IndexError, TypeError):
      # Now ord(buf[p:p+1]) == ord('') gets TypeError.
      raise message_mod.DecodeError('Truncated message.')
    except struct.error as e:
      raise message_mod.DecodeError(e)
    return length   # Return this for legacy reasons.
  cls.MergeFromString = MergeFromString

  fields_by_tag = cls._fields_by_tag
  message_set_decoders_by_tag = cls._message_set_decoders_by_tag

  def InternalParse(self, buffer, pos, end, current_depth=0):
    """Create a message from serialized bytes.

    Args:
      self: Message, instance of the proto message object.
      buffer: memoryview of the serialized data.
      pos: int, position to start in the serialized data.
      end: int, end position of the serialized data.

    Returns:
      Message object.
    """
    # Guard against internal misuse, since this function is called internally
    # quite extensively, and its easy to accidentally pass bytes.
    assert isinstance(buffer, memoryview)
    self._Modified()
    field_dict = self._fields
    while pos != end:
      (tag_bytes, new_pos) = decoder.ReadTag(buffer, pos)
      field_decoder, field_des = message_set_decoders_by_tag.get(
          tag_bytes, (None, None)
      )
      if field_decoder:
        pos = field_decoder(
            buffer, new_pos, end, self, field_dict, current_depth
        )
        continue
      field_des, is_packed = fields_by_tag.get(tag_bytes, (None, None))
      if field_des is None:
        if not self._unknown_fields:   # pylint: disable=protected-access
          self._unknown_fields = []    # pylint: disable=protected-access
        field_number, wire_type = decoder.DecodeTag(tag_bytes)
        if field_number == 0:
          raise message_mod.DecodeError('Field number 0 is illegal.')
        (data, new_pos) = decoder._DecodeUnknownField(
            buffer, new_pos, end, field_number, wire_type
        )  # pylint: disable=protected-access
        if new_pos == -1:
          return pos
        self._unknown_fields.append(
            (tag_bytes, buffer[pos + len(tag_bytes) : new_pos].tobytes())
        )
        pos = new_pos
      else:
        _MaybeAddDecoder(cls, field_des)
        field_decoder = field_des._decoders[is_packed]
        pos = field_decoder(
            buffer, new_pos, end, self, field_dict, current_depth
        )
        if field_des.containing_oneof:
          self._UpdateOneofState(field_des)
    return pos

  cls._InternalParse = InternalParse

