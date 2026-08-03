import functools

def _wrap_setattr(setattr_fn):
  """`__setattr__` wrapper."""

  @functools.wraps(setattr_fn)
  def new_setattr(self, name, value):
    if not hasattr(self, '_epy_is_init_done'):
      raise ValueError(
          'Child of `@epy.frozen` class should be `@epy.frozen` too. (Error'
          f' raised by {type(self)})'
      )
    if not self._epy_is_init_done:  # pylint: disable=protected-access
      return setattr_fn(self, name, value)
    else:
      raise AttributeError(
          f'Cannot assign {name!r} in `@epy.frozen` class {type(self)}'
      )

  return new_setattr

