
def has_default_repr(cls: Any) -> bool:
  """Returns `True` if the dataclass do not overwrite `__repr__`."""
  repr_fn = inspect.unwrap(cls.__repr__)
  return repr_fn.__qualname__ == '__create_fn__.<locals>.__repr__'

