
def _make_kw_only(cls: _ClsT) -> _ClsT:
  """Replace the `__init__` by a keyword-only version."""
  # Use `cls.__dict__` and not `hasattr` to ignore parent classes
  if '__init__' not in cls.__dict__:
    return cls  # Do not mutate the class if __init__ isn't present

  old_init = cls.__init__

  # Despite `@functools.wraps`, the function has to be called `__init__` (
  # see: https://stackoverflow.com/q/29919804/4172685)
  @functools.wraps(old_init)
  def __init__(self, *args, **kwargs):  # pylint: disable=invalid-name
    if args:
      raise TypeError(
          f'{self.__class__.__name__} contructor is keyword-only. '
          f'Got {len(args)} positional arguments.'
      )
    return old_init(self, **kwargs)

  cls.__init__ = __init__

  return cls

