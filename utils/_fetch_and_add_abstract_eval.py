
def _fetch_and_add_abstract_eval(*args):
  x_ref, value, *indices, subcore_id = args
  if x_ref.dtype != jnp.int32:
    raise NotImplementedError(
        f"Only int32 refs are supported, but got {x_ref.dtype}"
    )
  if x_ref.memory_space != tpu_core.MemorySpace.SMEM:
    raise ValueError(
        f"Only refs in SMEM memory space are supported, but got {x_ref}"
    )
  if value.dtype != x_ref.dtype or value.shape:
    raise ValueError(
        "The value must be a scalar of the same type as the ref"
        f" ({x_ref.dtype}), but got {value}."
    )
  if any(i.dtype != jnp.int32 or i.shape for i in indices):
    raise ValueError(
        f"All indices must be scalars of type int32, but got {indices}."
    )
  if subcore_id.dtype != jnp.int32 or subcore_id.shape:
    raise ValueError(
        f"subcore_id= must be a scalar of type int32, but got {subcore_id}."
    )
  return value, {state_types.ReadEffect(0), state_types.WriteEffect(0)}

