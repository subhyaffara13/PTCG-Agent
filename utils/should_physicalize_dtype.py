
def should_physicalize_dtype(dtype: DTypeLike) -> bool:
  """Returns whether a dtype should be lowered to a physical type."""
  return (
      jnp.issubdtype(dtype, dtypes.extended) and
      not any(jnp.issubdtype(dtype, t) for t in PHYSICAL_EXTENDED_DTYPES)
  )

