
def MessageToDict(
    message,
    always_print_fields_with_no_presence=False,
    preserving_proto_field_name=False,
    use_integers_for_enums=False,
    descriptor_pool=None,
    *,
    unquote_int64_if_possible=False,
):
  """Converts protobuf message to a dictionary.

  When the dictionary is encoded to JSON, it conforms to ProtoJSON spec.

  Args:
    message: The protocol buffers message instance to serialize.
    always_print_fields_with_no_presence: If True, fields without presence
      (implicit presence scalars, repeated fields, and map fields) will always
      be serialized. Any field that supports presence is not affected by this
      option (including singular message fields and oneof fields).
    preserving_proto_field_name: If True, use the original proto field names as
      defined in the .proto file. If False, convert the field names to
      lowerCamelCase.
    use_integers_for_enums: If true, print integers instead of enum names.
    descriptor_pool: A Descriptor Pool for resolving types. If None use the
      default.
    unquote_int64_if_possible: If True, unquote int64 fields for values that
      are safe to emit as numbers (all values smaller than 2^53 and a sparse
      set of values that are larger).

  Returns:
    A dict representation of the protocol buffer message.
  """
  printer = _Printer(
      preserving_proto_field_name,
      use_integers_for_enums,
      descriptor_pool,
      always_print_fields_with_no_presence,
      unquote_int64_if_possible=unquote_int64_if_possible,
  )
  # pylint: disable=protected-access
  return printer._MessageToJsonObject(message)

