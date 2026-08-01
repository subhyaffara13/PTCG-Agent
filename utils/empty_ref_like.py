
def empty_ref_like(x: object) -> jax_typing.Array:
  """Returns an empty array Ref with same shape/dtype/memory space as x."""
  match x:
    case pl_core.MemoryRef():
      memory_space = x.memory_space
    case jax_core.ShapeDtypeStruct():
      memory_space = pl_core.MemorySpace.ANY
    case _:
      raise ValueError(f'empty_ref_like does not support {type(x)}')
  return jax_core.new_ref(empty_like(x), memory_space=memory_space)

