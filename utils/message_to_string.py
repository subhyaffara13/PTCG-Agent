
def MessageToString(
    message,
    as_utf8=_as_utf8_default,
    as_one_line=False,
    use_short_repeated_primitives=False,
    pointy_brackets=False,
    use_index_order=False,
    use_field_number=False,
    descriptor_pool=None,
    indent=0,
    message_formatter=None,
    print_unknown_fields=False,
    force_colon=False) -> str:
  """Convert protobuf message to text format.

  Args:
    message: The protocol buffers message.
    as_utf8: Return unescaped Unicode for non-ASCII characters.
    as_one_line: Don't introduce newlines between fields.
    use_short_repeated_primitives: Use short repeated format for primitives.
    pointy_brackets: If True, use angle brackets instead of curly braces for
      nesting.
    use_index_order: If True, fields of a proto message will be printed using
      the order defined in source code instead of the field number, extensions
      will be printed at the end of the message and their relative order is
      determined by the extension number. By default, use the field number
      order.
    use_field_number: If True, print field numbers instead of names.
    descriptor_pool (DescriptorPool): Descriptor pool used to resolve Any types.
    indent (int): The initial indent level, in terms of spaces, for pretty
      print.
    message_formatter (function(message, indent, as_one_line) -> unicode|None):
      Custom formatter for selected sub-messages (usually based on message
      type). Use to pretty print parts of the protobuf for easier diffing.
    print_unknown_fields: If True, unknown fields will be printed.
    force_colon: If set, a colon will be added after the field name even if the
      field is a proto message.

  Returns:
    str: A string of the text formatted protocol buffer message.
  """
  out = TextWriter(as_utf8)
  printer = _Printer(
      out=out,
      indent=indent,
      as_utf8=as_utf8,
      as_one_line=as_one_line,
      use_short_repeated_primitives=use_short_repeated_primitives,
      pointy_brackets=pointy_brackets,
      use_index_order=use_index_order,
      use_field_number=use_field_number,
      descriptor_pool=descriptor_pool,
      message_formatter=message_formatter,
      print_unknown_fields=print_unknown_fields,
      force_colon=force_colon,
  )
  printer.PrintMessage(message)
  result = out.getvalue()
  out.close()
  if as_one_line:
    return result.rstrip()
  return result

