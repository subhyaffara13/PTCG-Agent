
def register_flag_parser_for_type(
    field_type: _T, parser: flags.ArgumentParser) -> _T:
  """Registers parser for a given type.

  See documentation for `register_flag_parser` for usage example.

  Args:
    field_type: field type to register
    parser: parser to use

  Returns:
    field_type unmodified.
  """
  _FIELD_TYPE_TO_PARSER[field_type] = parser
  return field_type

