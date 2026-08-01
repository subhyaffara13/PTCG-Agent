
def _ExtractSymbols(
    desc_proto: 'descriptor_pb2.DescriptorProto', package: str
) -> Iterator[str]:
  """Pulls out all the symbols from a descriptor proto.

  Args:
    desc_proto: The proto to extract symbols from.
    package: The package containing the descriptor type.

  Yields:
    The fully qualified name found in the descriptor.
  """
  message_name = package + '.' + desc_proto.name if package else desc_proto.name
  yield message_name
  for nested_type in desc_proto.nested_type:
    for symbol in _ExtractSymbols(nested_type, message_name):
      yield symbol
  for enum_type in desc_proto.enum_type:
    yield '.'.join((message_name, enum_type.name))

