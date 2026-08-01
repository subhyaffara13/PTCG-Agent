
def typeof(x: Any) -> Any:
  """Return the JAX type (i.e. :class:`AbstractValue`) of the input.

  Raises a ``TypeError`` if ``x`` is not a valid JAX type.
  """
  typ = type(x)
  if (aval_fn := pytype_aval_mappings.get(typ)):  # fast path
    return aval_fn(x)
  for t in typ.__mro__[1:]:
    if (aval_fn := pytype_aval_mappings.get(t)):
      return aval_fn(x)
  if getattr(x, '__jax_array__', None) is not None:
    raise ValueError(
        'Triggering __jax_array__() during abstractification is no longer'
        ' supported. To avoid this error, either explicitly convert your object'
        ' using jax.numpy.array(), or register your object as a pytree.'
    )
  raise TypeError(f"Argument '{x}' of type '{typ}' is not a valid JAX type")

