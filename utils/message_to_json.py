
def MessageToJson(
    message,
    preserving_proto_field_name=False,
    indent=2,
    sort_keys=False,
    use_integers_for_enums=False,
    descriptor_pool=None,
    ensure_ascii=True,
    always_print_fields_with_no_presence=False,
    *,
    unquote_int64_if_possible=False,
):
  """Converts protobuf message to JSON format.

  Args:
    message: The protocol buffers message instance to serialize.
    always_print_fields_with_no_presence: If True, fields without presence
      (implicit presence scalars, repeated fields, and map fields) will always
      be serialized. Any field that supports presence is not affected by this
      option (including singular message fields and oneof fields).
    preserving_proto_field_name: If True, use the original proto field names as
      defined in the .proto file. If False, convert the field names to
      lowerCamelCase.
    indent: The JSON object will be pretty-printed with this indent level. An
      indent level of 0 or negative will only insert newlines. If the indent
      level is None, no newlines will be inserted.
    sort_keys: If True, then the output will be sorted by field names.
    use_integers_for_enums: If true, print integers instead of enum names.
    descriptor_pool: A Descriptor Pool for resolving types. If None use the
      default.
    ensure_ascii: If True, strings with non-ASCII characters are escaped. If
      False, Unicode strings are returned unchanged.
    unquote_int64_if_possible: If True, unquote int64 fields for values that
      are safe to emit as numbers (all values smaller than 2^53 and a sparse
      set of values that are larger).

  Returns:
    A string containing the JSON formatted protocol buffer message.
  """
  printer = _Printer(
      preserving_proto_field_name,
      use_integers_for_enums,
      descriptor_pool,
      always_print_fields_with_no_presence,
      unquote_int64_if_possible=unquote_int64_if_possible,
  )
  return printer.ToJsonString(message, indent, sort_keys, ensure_ascii)

