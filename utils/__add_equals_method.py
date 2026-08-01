
def _AddEqualsMethod(message_descriptor, cls):
  """Helper for _AddMessageMethods()."""
  def __eq__(self, other):
    if self.DESCRIPTOR.full_name == _ListValueFullTypeName and isinstance(
        other, list
    ):
      return self._internal_compare(other)
    if self.DESCRIPTOR.full_name == _StructFullTypeName and isinstance(
        other, dict
    ):
      return self._internal_compare(other)

    if (not isinstance(other, message_mod.Message) or
        other.DESCRIPTOR != self.DESCRIPTOR):
      return NotImplemented

    if self is other:
      return True

    if self.DESCRIPTOR.full_name == _AnyFullTypeName:
      any_a = _InternalUnpackAny(self)
      any_b = _InternalUnpackAny(other)
      if any_a and any_b:
        return any_a == any_b

    if not self.ListFields() == other.ListFields():
      return False

    # TODO: Fix UnknownFieldSet to consider MessageSet extensions,
    # then use it for the comparison.
    unknown_fields = list(self._unknown_fields)
    unknown_fields.sort()
    other_unknown_fields = list(other._unknown_fields)
    other_unknown_fields.sort()
    return unknown_fields == other_unknown_fields

  cls.__eq__ = __eq__

