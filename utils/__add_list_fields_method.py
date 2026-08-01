
def _AddListFieldsMethod(message_descriptor, cls):
  """Helper for _AddMessageMethods()."""

  def ListFields(self):
    all_fields = [item for item in self._fields.items() if _IsPresent(item)]
    all_fields.sort(key = lambda item: item[0].number)
    return all_fields

  cls.ListFields = ListFields

