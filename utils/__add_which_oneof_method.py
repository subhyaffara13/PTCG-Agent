
def _AddWhichOneofMethod(message_descriptor, cls):
  def WhichOneof(self, oneof_name):
    """Returns the name of the currently set field inside a oneof, or None."""
    try:
      field = message_descriptor.oneofs_by_name[oneof_name]
    except KeyError:
      raise ValueError(
          'Protocol message has no oneof "%s" field.' % oneof_name)

    nested_field = self._oneofs.get(field, None)
    if nested_field is not None and self.HasField(nested_field.name):
      return nested_field.name
    else:
      return None

  cls.WhichOneof = WhichOneof

