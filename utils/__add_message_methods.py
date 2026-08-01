
def _AddMessageMethods(message_descriptor, cls):
  """Adds implementations of all Message methods to cls."""
  _AddListFieldsMethod(message_descriptor, cls)
  _AddHasFieldMethod(message_descriptor, cls)
  _AddClearFieldMethod(message_descriptor, cls)
  if message_descriptor.is_extendable:
    _AddClearExtensionMethod(cls)
    _AddHasExtensionMethod(cls)
  _AddEqualsMethod(message_descriptor, cls)
  _AddStrMethod(message_descriptor, cls)
  _AddReprMethod(message_descriptor, cls)
  _AddUnicodeMethod(message_descriptor, cls)
  _AddContainsMethod(message_descriptor, cls)
  _AddByteSizeMethod(message_descriptor, cls)
  _AddSerializeToStringMethod(message_descriptor, cls)
  _AddSerializePartialToStringMethod(message_descriptor, cls)
  _AddMergeFromStringMethod(message_descriptor, cls)
  _AddIsInitializedMethod(message_descriptor, cls)
  _AddMergeFromMethod(cls)
  _AddWhichOneofMethod(message_descriptor, cls)
  # Adds methods which do not depend on cls.
  cls.Clear = _Clear
  cls.DiscardUnknownFields = _DiscardUnknownFields
  cls._SetListener = _SetListener

