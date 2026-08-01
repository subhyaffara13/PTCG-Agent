
def _AddSerializeToStringMethod(message_descriptor, cls):
  """Helper for _AddMessageMethods()."""

  def SerializeToString(self, **kwargs):
    # Check if the message has all of its required fields set.
    if not self.IsInitialized():
      raise message_mod.EncodeError(
          'Message %s is missing required fields: %s' % (
          self.DESCRIPTOR.full_name, ','.join(self.FindInitializationErrors())))
    return self.SerializePartialToString(**kwargs)
  cls.SerializeToString = SerializeToString

