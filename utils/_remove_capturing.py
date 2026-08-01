
def _remove_capturing(cls):
  """Remove capturing methods from a Module."""
  for name, method in cls.__dict__.items():
    if hasattr(method, '_does_capturing'):
      setattr(cls, name, method.__wrapped__)
  return cls

