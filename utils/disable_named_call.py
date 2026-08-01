
def disable_named_call():
  """Disables named call wrapping.

  See ``enable_named_call``
  """
  global _use_named_call
  _use_named_call = False

