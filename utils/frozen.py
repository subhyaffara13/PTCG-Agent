
def frozen(_, __, ___):
    """
    Prevent an attribute to be modified.

    .. versionadded:: 20.1.0
    """
    raise FrozenAttributeError


def frozen(cls: type[_T]) -> type[_T]:
    cls.__init_subclass__ = _do_not_subclass
    return _frozen(cls)


def frozen(*args, **kwargs):
    """Dummy method for raising errors when trying to modify frozen graphs"""
    raise nx.NetworkXError("Frozen graph can't be modified")


def frozen(self: _T) -> _T:
  """Freeze the dataclass."""
  del self
  raise ValueError('`.frozen()` can only be called after `.unfrozen()`.')


def frozen(cls: _Cls) -> _Cls:
  """Class decorator which prevent mutating attributes after `__init__`.

  Example:

  ```python
  @epy.frozen
  class A:

    def __init__(self):
      self.x = 123

  a = A()
  a.x = 456  # AttributeError
  ```

  Supports inheritance, child classes should explicitly be marked as
  `@epy.frozen` if they mutate additional attributes in `__init__`.

  Args:
    cls: The class to freeze.

  Returns:
    cls: The class object
  """
  if not isinstance(cls, type):
    raise TypeError(f'{cls.__name__} is not')

  cls.__init__ = _wrap_init(cls.__init__)
  cls.__setattr__ = _wrap_setattr(cls.__setattr__)
  return cls

