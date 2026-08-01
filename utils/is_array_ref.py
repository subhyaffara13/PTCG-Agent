
def is_array_ref(x) -> tp.TypeGuard[Ref]:
  return isinstance(x, jax.Array | AbstractRef | Ref) and isinstance(
    jax.typeof(x), AbstractRef | Ref
  )

