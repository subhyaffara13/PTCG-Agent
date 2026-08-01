
def PrintMessage(message,
                 out,
                 indent=0,
                 as_utf8=_as_utf8_default,
                 as_one_line=False,
                 use_short_repeated_primitives=False,
                 pointy_brackets=False,
                 use_index_order=False,
                 use_field_number=False,
                 descriptor_pool=None,
                 message_formatter=None,
                 print_unknown_fields=False,
                 force_colon=False):
  """Convert the message to text format and write it to the out stream.

  Args:
    message: The Message object to convert to text format.
    out: A file handle to write the message to.
    indent: The initial indent level for pretty print.
    as_utf8: Return unescaped Unicode for non-ASCII characters.
    as_one_line: Don't introduce newlines between fields.
    use_short_repeated_primitives: Use short repeated format for primitives.
    pointy_brackets: If True, use angle brackets instead of curly braces for
      nesting.
    use_index_order: If True, print fields of a proto message using the order
      defined in source code instead of the field number. By default, use the
      field number order.
    use_field_number: If True, print field numbers instead of names.
    descriptor_pool: A DescriptorPool used to resolve Any types.
    message_formatter: A function(message, indent, as_one_line): unicode|None
      to custom format selected sub-messages (usually based on message type).
      Use to pretty print parts of the protobuf for easier diffing.
    print_unknown_fields: If True, unknown fields will be printed.
    force_colon: If set, a colon will be added after the field name even if
      the field is a proto message.
  """
  printer = _Printer(
      out=out, indent=indent, as_utf8=as_utf8,
      as_one_line=as_one_line,
      use_short_repeated_primitives=use_short_repeated_primitives,
      pointy_brackets=pointy_brackets,
      use_index_order=use_index_order,
      use_field_number=use_field_number,
      descriptor_pool=descriptor_pool,
      message_formatter=message_formatter,
      print_unknown_fields=print_unknown_fields,
      force_colon=force_colon)
  printer.PrintMessage(message)

