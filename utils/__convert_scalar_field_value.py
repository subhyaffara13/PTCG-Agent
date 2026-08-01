
def _ConvertScalarFieldValue(value, field, path, require_str=False):
  """Convert a single scalar field value.

  Args:
    value: A scalar value to convert the scalar field value.
    field: The descriptor of the field to convert.
    path: parent path to log parse error info.
    require_str: If True, the field value must be a str.

  Returns:
    The converted scalar field value

  Raises:
    ParseError: In case of convert problems.
    EnumStringValueParseError: In case of unknown enum string value.
  """
  try:
    if field.cpp_type in _INT_TYPES:
      return _ConvertInteger(value)
    elif field.cpp_type in _FLOAT_TYPES:
      return _ConvertFloat(value, field)
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_BOOL:
      return _ConvertBool(value, require_str)
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_STRING:
      if field.type == descriptor.FieldDescriptor.TYPE_BYTES:
        if isinstance(value, str):
          encoded = value.encode('utf-8')
        else:
          encoded = value
        # Add extra padding '='
        padded_value = encoded + b'=' * (4 - len(encoded) % 4)
        return base64.urlsafe_b64decode(padded_value)
      else:
        # Checking for unpaired surrogates appears to be unreliable,
        # depending on the specific Python version, so we check manually.
        if _UNPAIRED_SURROGATE_PATTERN.search(value):
          raise ParseError('Unpaired surrogate')
        return value
    elif field.cpp_type == descriptor.FieldDescriptor.CPPTYPE_ENUM:
      # Convert an enum value.
      enum_value = field.enum_type.values_by_name.get(value, None)
      if enum_value is None:
        try:
          number = int(value)
          enum_value = field.enum_type.values_by_number.get(number, None)
        except ValueError as e:
          # Since parsing to integer failed and lookup in values_by_name didn't
          # find this name, we have an enum string value which is unknown.
          raise EnumStringValueParseError(
              'Invalid enum value {0} for enum type {1}'.format(
                  value, field.enum_type.full_name
              )
          ) from e
        if enum_value is None:
          if field.enum_type.is_closed:
            raise ParseError(
                'Invalid enum value {0} for enum type {1}'.format(
                    value, field.enum_type.full_name
                )
            )
          else:
            return number
      return enum_value.number
  except EnumStringValueParseError as e:
    raise EnumStringValueParseError('{0} at {1}'.format(e, path)) from e
  except ParseError as e:
    raise ParseError('{0} at {1}'.format(e, path)) from e

