
def shaped_abstractify(x):
  typ = type(x)
  if (aval_fn := pytype_aval_mappings.get(typ)):  # fast path
    return aval_fn(x)
  for t in typ.__mro__[1:]:
    if (aval_fn := pytype_aval_mappings.get(t)):
      return aval_fn(x)
  if isinstance(x, AbstractValue):
    return x
  if getattr(x, '__jax_array__', None) is not None:
    raise ValueError(
        'Triggering __jax_array__() during abstractification is no longer'
        ' supported. To avoid this error, either explicitly convert your object'
        ' using jax.numpy.array(), or register your object as a pytree.'
    )
  if hasattr(x, 'dtype'):
    aval = ShapedArray(
        np.shape(x),
        dtypes.canonicalize_dtype(x.dtype, allow_extended_dtype=True),
        weak_type=getattr(x, "weak_type", False),
    )
    return update_aval_with_sharding(aval, getattr(x, 'sharding', None))
  raise TypeError(
      f"Cannot interpret value of type {typ} as an abstract array; it "
      "does not have a dtype attribute")

