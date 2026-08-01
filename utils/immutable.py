
def immutable(cls):
  """Decorator to avoid boilerplate for immutable interned classes."""
  def __deepcopy__(self, memo):
    # Deep copy of a singleton interned object is the identity.
    return self
  cls.__deepcopy__ = __deepcopy__

  # Pickling calls __getstate__ and __setstate__, but we're assuming the
  # caller will implement __getnewargs_ex__.
  def __getstate__(self):
    return None
  def __setstate__(self, state):
    pass
  cls.__getstate__ = __getstate__
  cls.__setstate__ = __setstate__

  # Discourage mutation after construction.
  def __setattr__(self, name, value):
    raise AttributeError(f"cannot assign to field {name!r}")
  def __delattr__(self, name):
    raise AttributeError(f"cannot delete field {name!r}")
  cls.__setattr__ = __setattr__
  cls.__delattr__ = __delattr__
  return cls

