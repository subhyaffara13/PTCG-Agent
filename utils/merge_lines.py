
def MergeLines(lines,
               message,
               allow_unknown_extension=False,
               allow_field_number=False,
               descriptor_pool=None,
               allow_unknown_field=False,
               max_recursion_depth=None):
  """Parses a text representation of a protocol message into a message.

  See Merge() for more details.

  Args:
    lines: An iterable of lines of a message's text representation.
    message: A protocol buffer message to merge into.
    allow_unknown_extension: if True, skip over missing extensions and keep
      parsing
    allow_field_number: if True, both field number and field name are allowed.
    descriptor_pool: A DescriptorPool used to resolve Any types.
    allow_unknown_field: if True, skip over unknown field and keep
      parsing. Avoid to use this option if possible. It may hide some
      errors (e.g. spelling error on field name)
    max_recursion_depth: Optional maximum recursion depth of a text proto
      message to be deserialized. Text proto messages over this depth will
      fail to parse. ``None`` keeps the historical unbounded behavior.

  Returns:
    The same message passed as argument.

  Raises:
    ParseError: On text parsing problems.
  """
  parser = _Parser(allow_unknown_extension,
                   allow_field_number,
                   descriptor_pool=descriptor_pool,
                   allow_unknown_field=allow_unknown_field,
                   max_recursion_depth=max_recursion_depth)
  return parser.MergeLines(lines, message)

