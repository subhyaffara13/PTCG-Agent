
def _AddContainsMethod(message_descriptor, cls):

  if message_descriptor.full_name == 'google.protobuf.Struct':
    def __contains__(self, key):
      return key in self.fields
  elif message_descriptor.full_name == 'google.protobuf.ListValue':
    def __contains__(self, value):
      return value in self.items()
  else:
    def __contains__(self, field):
      return self.HasField(field)

  cls.__contains__ = __contains__

