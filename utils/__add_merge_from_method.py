
def _AddMergeFromMethod(cls):
  CPPTYPE_MESSAGE = _FieldDescriptor.CPPTYPE_MESSAGE

  def MergeFrom(self, msg):
    if not isinstance(msg, cls):
      raise TypeError(
          'Parameter to MergeFrom() must be instance of same class: '
          'expected %s got %s.' % (_FullyQualifiedClassName(cls),
                                   _FullyQualifiedClassName(msg.__class__)))

    assert msg is not self
    self._Modified()

    fields = self._fields

    for field, value in msg._fields.items():
      if field.is_repeated:
        field_value = fields.get(field)
        if field_value is None:
          # Construct a new object to represent this field.
          field_value = field._default_constructor(self)
          fields[field] = field_value
        field_value.MergeFrom(value)
      elif field.cpp_type == CPPTYPE_MESSAGE:
        if value._is_present_in_parent:
          field_value = fields.get(field)
          if field_value is None:
            # Construct a new object to represent this field.
            field_value = field._default_constructor(self)
            fields[field] = field_value
          field_value.MergeFrom(value)
      else:
        self._fields[field] = value
        if field.containing_oneof:
          self._UpdateOneofState(field)

    if msg._unknown_fields:
      if not self._unknown_fields:
        self._unknown_fields = []
      self._unknown_fields.extend(msg._unknown_fields)

  cls.MergeFrom = MergeFrom

