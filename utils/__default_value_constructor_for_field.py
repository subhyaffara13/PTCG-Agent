
def _DefaultValueConstructorForField(field):
  """Returns a function which returns a default value for a field.

  Args:
    field: FieldDescriptor object for this field.

  The returned function has one argument:
    message: Message instance containing this field, or a weakref proxy
      of same.

  That function in turn returns a default value for this field.  The default
    value may refer back to |message| via a weak reference.
  """

  if _IsMapField(field):
    return _GetInitializeDefaultForMap(field)

  if field.is_repeated:
    if field.has_default_value and field.default_value != []:
      raise ValueError('Repeated field default value not empty list: %s' % (
          field.default_value))
    if field.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
      # We can't look at _concrete_class yet since it might not have
      # been set.  (Depends on order in which we initialize the classes).
      message_type = field.message_type
      def MakeRepeatedMessageDefault(message):
        return containers.RepeatedCompositeFieldContainer(
            message._listener_for_children, field.message_type)
      return MakeRepeatedMessageDefault
    else:
      type_checker = type_checkers.GetTypeChecker(field)
      def MakeRepeatedScalarDefault(message):
        return containers.RepeatedScalarFieldContainer(
            message._listener_for_children, type_checker, field
        )
      return MakeRepeatedScalarDefault

  if field.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
    message_type = field.message_type
    def MakeSubMessageDefault(message):
      # _concrete_class may not yet be initialized.
      if not hasattr(message_type, '_concrete_class'):
        from google.protobuf import message_factory
        message_factory.GetMessageClass(message_type)
      result = message_type._concrete_class()
      result._SetListener(
          _OneofListener(message, field)
          if field.containing_oneof is not None
          else message._listener_for_children)
      return result
    return MakeSubMessageDefault

  def MakeScalarDefault(message):
    # TODO: This may be broken since there may not be
    # default_value.  Combine with has_default_value somehow.
    return field.default_value
  return MakeScalarDefault

