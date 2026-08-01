
def _AddClearFieldMethod(message_descriptor, cls):
  """Helper for _AddMessageMethods()."""
  def ClearField(self, field_name):
    try:
      field = message_descriptor.fields_by_name[field_name]
    except KeyError:
      try:
        field = message_descriptor.oneofs_by_name[field_name]
        if field in self._oneofs:
          field = self._oneofs[field]
        else:
          return
      except KeyError:
        raise ValueError('Protocol message %s has no "%s" field.' %
                         (message_descriptor.name, field_name))

    if field in self._fields:
      # To match the C++ implementation, we need to invalidate iterators
      # for map fields when ClearField() happens.
      if hasattr(self._fields[field], 'InvalidateIterators'):
        self._fields[field].InvalidateIterators()

      # Note:  If the field is a sub-message, its listener will still point
      #   at us.  That's fine, because the worst than can happen is that it
      #   will call _Modified() and invalidate our byte size.  Big deal.
      del self._fields[field]

      if self._oneofs.get(field.containing_oneof, None) is field:
        del self._oneofs[field.containing_oneof]

    # Always call _Modified() -- even if nothing was changed, this is
    # a mutating method, and thus calling it should cause the field to become
    # present in the parent message.
    self._Modified()

  cls.ClearField = ClearField

