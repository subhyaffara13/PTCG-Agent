
def _from_value_representation(x: _ValueRepresentation) -> Any:
  if isinstance(x, _ArrayRepresentation):
    return jax.ShapeDtypeStruct(x.shape, x.dtype)

  elif isinstance(x, _PartitionedArrayRepresentation):
    return jax.ShapeDtypeStruct(
      x.array_representation.shape, x.array_representation.dtype
    )

  elif isinstance(x, _ObjectRepresentation):
    return x.obj

  raise TypeError(x, type(x))

