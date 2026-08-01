
def _AddPropertiesForNonRepeatedScalarField(field, cls):
  """Adds a public property for a nonrepeated, scalar protocol message field.
  Clients can use this property to get and directly set the value of the field.
  Note that when the client sets the value of a field by using this property,
  all necessary "has" bits are set as a side-effect, and we also perform
  type-checking.

  Args:
    field: A FieldDescriptor for this field.
    cls: The class we're constructing.
  """
  proto_field_name = field.name
  property_name = _PropertyName(proto_field_name)
  type_checker = type_checkers.GetTypeChecker(field)
  default_value = field.default_value

  def getter(self):
    # TODO: This may be broken since there may not be
    # default_value.  Combine with has_default_value somehow.
    return self._fields.get(field, default_value)
  getter.__module__ = None
  getter.__doc__ = 'Getter for %s.' % proto_field_name

  def field_setter(self, new_value):
    # pylint: disable=protected-access
    # Testing the value for truthiness captures all of the implicit presence
    # defaults (0, 0.0, enum 0, and False), except for -0.0.
    try:
      new_value = type_checker.CheckValue(new_value)
    except TypeError as e:
      raise TypeError(
          'Cannot set %s to %.1024r: %s' % (field.full_name, new_value, e))
    if not field.has_presence and decoder.IsDefaultScalarValue(new_value):
      self._fields.pop(field, None)
    else:
      self._fields[field] = new_value
    # Check _cached_byte_size_dirty inline to improve performance, since scalar
    # setters are called frequently.
    if not self._cached_byte_size_dirty:
      self._Modified()

  if field.containing_oneof:
    def setter(self, new_value):
      field_setter(self, new_value)
      self._UpdateOneofState(field)
  else:
    setter = field_setter

  setter.__module__ = None
  setter.__doc__ = 'Setter for %s.' % proto_field_name

  # Add a property to encapsulate the getter/setter.
  doc = 'Magic attribute generated for "%s" proto field.' % proto_field_name
  setattr(cls, property_name, _FieldProperty(field, getter, setter, doc=doc))

