
def _AddPropertiesForNonRepeatedCompositeField(field, cls):
  """Adds a public property for a nonrepeated, composite protocol message field.
  A composite field is a "group" or "message" field.

  Clients can use this property to get the value of the field, but cannot
  assign to the property directly.

  Args:
    field: A FieldDescriptor for this field.
    cls: The class we're constructing.
  """
  # TODO: Remove duplication with similar method
  # for non-repeated scalars.
  proto_field_name = field.name
  property_name = _PropertyName(proto_field_name)

  def getter(self):
    field_value = self._fields.get(field)
    if field_value is None:
      # Construct a new object to represent this field.
      field_value = field._default_constructor(self)

      # Atomically check if another thread has preempted us and, if not, swap
      # in the new object we just created.  If someone has preempted us, we
      # take that object and discard ours.
      # WARNING:  We are relying on setdefault() being atomic.  This is true
      #   in CPython but we haven't investigated others.  This warning appears
      #   in several other locations in this file.
      field_value = self._fields.setdefault(field, field_value)
    return field_value
  getter.__module__ = None
  getter.__doc__ = 'Getter for %s.' % proto_field_name

  # We define a setter just so we can throw an exception with a more
  # helpful error message.
  def setter(self, new_value):
    if field.message_type.full_name == 'google.protobuf.Timestamp':
      getter(self)
      self._fields[field].FromDatetime(new_value)
    elif field.message_type.full_name == 'google.protobuf.Duration':
      getter(self)
      self._fields[field].FromTimedelta(new_value)
    elif field.message_type.full_name == _StructFullTypeName:
      getter(self)
      self._fields[field].Clear()
      self._fields[field].update(new_value)
    elif field.message_type.full_name == _ListValueFullTypeName:
      getter(self)
      self._fields[field].Clear()
      self._fields[field].extend(new_value)
    else:
      raise AttributeError(
          'Assignment not allowed to composite field '
          '"%s" in protocol message object.' % proto_field_name
      )

  # Add a property to encapsulate the getter.
  doc = 'Magic attribute generated for "%s" proto field.' % proto_field_name
  setattr(cls, property_name, _FieldProperty(field, getter, setter, doc=doc))

