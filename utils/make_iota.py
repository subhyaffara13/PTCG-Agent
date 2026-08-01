
def make_iota(axis_size: AxisSize) -> Array:
  # Callers of this utility, via batch() or vtile(), must be in a context
  # where lax is importable.
  from jax import lax  # pyrefly: ignore[missing-module-attribute]
  handler = make_iota_handlers.get(type(axis_size))
  if handler:
    return handler(axis_size)
  else:
    return lax.iota('int32', int(axis_size))

