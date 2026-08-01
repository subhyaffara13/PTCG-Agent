
def _AddInitMethod(message_descriptor, cls):
  """Adds an __init__ method to cls."""

  def _GetIntegerEnumValue(enum_type, value):
    """Convert a string or integer enum value to an integer.

    If the value is a string, it is converted to the enum value in
    enum_type with the same name.  If the value is not a string, it's
    returned as-is.  (No conversion or bounds-checking is done.)
    """
    if isinstance(value, str):
      try:
        return enum_type.values_by_name[value].number
      except KeyError:
        raise ValueError('Enum type %s: unknown label "%s"' % (
            enum_type.full_name, value))
    return value

  def init(self, **kwargs):

    def init_wkt_or_merge(field, msg, value):
      if isinstance(value, message_mod.Message):
        msg.MergeFrom(value)
      elif (
          isinstance(value, dict)
          and field.message_type.full_name == _StructFullTypeName
      ):
        msg.Clear()
        if len(value) == 1 and 'fields' in value:
          try:
            msg.update(value)
          except:
            msg.Clear()
            msg.__init__(**value)
        else:
          msg.update(value)
      elif hasattr(msg, '_internal_assign'):
        msg._internal_assign(value)
      else:
        raise TypeError(
            'Message field {0}.{1} must be initialized with a '
            'dict or instance of same class, got {2}.'.format(
                message_descriptor.name,
                field.name,
                type(value).__name__,
            )
        )

    self._cached_byte_size = 0
    self._cached_byte_size_dirty = len(kwargs) > 0
    self._fields = {}
    # Contains a mapping from oneof field descriptors to the descriptor
    # of the currently set field in that oneof field.
    self._oneofs = {}

    # _unknown_fields is () when empty for efficiency, and will be turned into
    # a list if fields are added.
    self._unknown_fields = ()
    self._is_present_in_parent = False
    self._listener = message_listener_mod.NullMessageListener()
    self._listener_for_children = _Listener(self)
    for field_name, field_value in kwargs.items():
      field = _GetFieldByName(message_descriptor, field_name)
      if field is None:
        raise TypeError('%s() got an unexpected keyword argument "%s"' %
                        (message_descriptor.name, field_name))
      if field_value is None:
        # field=None is the same as no field at all.
        continue
      if field.is_repeated:
        field_copy = field._default_constructor(self)
        if field.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:  # Composite
          if _IsMapField(field):
            if _IsMessageMapField(field):
              for key in field_value:
                item_value = field_value[key]
                if isinstance(item_value, dict):
                  field_copy[key].__init__(**item_value)
                else:
                  field_copy[key].MergeFrom(item_value)
            else:
              field_copy.update(field_value)
          else:
            for val in field_value:
              if isinstance(val, dict) and (
                  field.message_type.full_name != _StructFullTypeName
              ):
                field_copy.add(**val)
              else:
                new_msg = field_copy.add()
                init_wkt_or_merge(field, new_msg, val)
        else:  # Scalar
          if field.cpp_type == _FieldDescriptor.CPPTYPE_ENUM:
            field_value = [_GetIntegerEnumValue(field.enum_type, val)
                           for val in field_value]
          field_copy.extend(field_value)
        self._fields[field] = field_copy
      elif field.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
        field_copy = field._default_constructor(self)
        if isinstance(field_value, dict) and (
            field.message_type.full_name != _StructFullTypeName
        ):
          new_val = field.message_type._concrete_class(**field_value)
          field_copy.MergeFrom(new_val)
        else:
          try:
            init_wkt_or_merge(field, field_copy, field_value)
          except TypeError:
            _ReraiseTypeErrorWithFieldName(message_descriptor.name, field_name)
        self._fields[field] = field_copy
      else:
        if field.cpp_type == _FieldDescriptor.CPPTYPE_ENUM:
          field_value = _GetIntegerEnumValue(field.enum_type, field_value)
        try:
          setattr(self, field_name, field_value)
        except TypeError:
          _ReraiseTypeErrorWithFieldName(message_descriptor.name, field_name)

  init.__module__ = None
  init.__doc__ = None
  cls.__init__ = init

