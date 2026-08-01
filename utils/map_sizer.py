
def MapSizer(field_descriptor, is_message_map):
  """Returns a sizer for a map field."""

  # Can't look at field_descriptor.message_type._concrete_class because it may
  # not have been initialized yet.
  message_type = field_descriptor.message_type
  message_sizer = MessageSizer(field_descriptor.number, False, False)

  def FieldSize(map_value):
    total = 0
    for key in map_value:
      value = map_value[key]
      # It's wasteful to create the messages and throw them away one second
      # later since we'll do the same for the actual encode.  But there's not an
      # obvious way to avoid this within the current design without tons of code
      # duplication. For message map, value.ByteSize() should be called to
      # update the status.
      entry_msg = message_type._concrete_class(key=key, value=value)
      total += message_sizer(entry_msg)
      if is_message_map:
        value.ByteSize()
    return total

  return FieldSize

