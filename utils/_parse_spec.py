
def _parse_spec(spec):
  """Parse an input spec of the form (shape, dtype) or shape into a jax.ShapeDtypeStruct."""
  spec = tuple(spec)
  if len(spec) == 2 and isinstance(spec[0], Iterable):
    return jax.ShapeDtypeStruct(tuple(spec[0]), spec[1])
  else:
    return jax.ShapeDtypeStruct(spec, jnp.float32)

