
def _AddStaticMethods(cls):

  def RegisterExtension(_):
    """no-op to keep generated code <=4.23 working with new runtimes."""
    # This was originally removed in 5.26 (cl/595989309).
    pass

  cls.RegisterExtension = staticmethod(RegisterExtension)
  def FromString(s):
    message = cls()
    message.MergeFromString(s)
    return message
  cls.FromString = staticmethod(FromString)

