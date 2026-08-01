
def GetMessageClassesForFiles(files, pool):
  """Gets all the messages from specified files.

  This will find and resolve dependencies, failing if the descriptor
  pool cannot satisfy them.

  This will not return the classes for nested types within those classes, for
  those, use GetMessageClass() on the nested types within their containing
  messages.

  For example, for the message:

  message NestedTypeMessage {
    message NestedType {
      string data = 1;
    }
    NestedType nested = 1;
  }

  NestedTypeMessage will be in the result, but not
  NestedTypeMessage.NestedType.

  Args:
    files: The file names to extract messages from.
    pool: The descriptor pool to find the files including the dependent files.

  Returns:
    A dictionary mapping proto names to the message classes.
  """
  result = {}
  for file_name in files:
    file_desc = pool.FindFileByName(file_name)
    for desc in file_desc.message_types_by_name.values():
      result[desc.full_name] = GetMessageClass(desc)

    # While the extension FieldDescriptors are created by the descriptor pool,
    # the python classes created in the factory need them to be registered
    # explicitly, which is done below.
    #
    # The call to RegisterExtension will specifically check if the
    # extension was already registered on the object and either
    # ignore the registration if the original was the same, or raise
    # an error if they were different.

    for extension in file_desc.extensions_by_name.values():
      _ = GetMessageClass(extension.containing_type)
      if api_implementation.Type() != 'python':
        # TODO: Remove this check here. Duplicate extension
        # register check should be in descriptor_pool.
        if extension is not pool.FindExtensionByNumber(
            extension.containing_type, extension.number
        ):
          raise ValueError('Double registration of Extensions')
      # Recursively load protos for extension field, in order to be able to
      # fully represent the extension. This matches the behavior for regular
      # fields too.
      if extension.message_type:
        GetMessageClass(extension.message_type)
  return result

