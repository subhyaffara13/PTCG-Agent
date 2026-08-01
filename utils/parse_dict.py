
def ParseDict(
    js_dict,
    message,
    ignore_unknown_fields=False,
    descriptor_pool=None,
    max_recursion_depth=100,
):
  """Parses a JSON dictionary representation into a message.

  Args:
    js_dict: Dict representation of a JSON message.
    message: A protocol buffer message to merge into.
    ignore_unknown_fields: If True, do not raise errors for unknown fields.
    descriptor_pool: A Descriptor Pool for resolving types. If None use the
      default.
    max_recursion_depth: max recursion depth of JSON message to be deserialized.
      JSON messages over this depth will fail to be deserialized. Default value
      is 100.

  Returns:
    The same message passed as argument.
  """
  parser = _Parser(ignore_unknown_fields, descriptor_pool, max_recursion_depth)
  parser.ConvertMessage(js_dict, message, '')
  return message

