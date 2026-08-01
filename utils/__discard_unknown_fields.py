
def _DiscardUnknownFields(self):
  self._unknown_fields = []
  for field, value in self.ListFields():
    if field.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
      if _IsMapField(field):
        if _IsMessageMapField(field):
          for key in value:
            value[key].DiscardUnknownFields()
      elif field.is_repeated:
        for sub_message in value:
          sub_message.DiscardUnknownFields()
      else:
        value.DiscardUnknownFields()

