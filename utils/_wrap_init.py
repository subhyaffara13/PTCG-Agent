import functools

def _wrap_init(init_fn):
  """`__init__` wrapper."""

  @functools.wraps(init_fn)
  def new_init(self, *args, **kwargs):
    # Do NOT use `hasattr` to support children with custom `__getattr__`
    if '_epy_is_init_done' in self.__dict__:
      # `_epy_is_init_done` already created, so it means we're
      # a `super().__init__` call.
      return init_fn(self, *args, **kwargs)
    object.__setattr__(self, '_epy_is_init_done', False)
    init_fn(self, *args, **kwargs)
    object.__setattr__(self, '_epy_is_init_done', True)

  return new_init

