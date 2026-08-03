from typing import Any

def with_memory_space_constraint(
    x: jax.Array, memory_space: Any
) -> jax.Array:
  """Constrains the memory space of an array.

  This primitive does not change the value of ``x``, but it constrains the
  memory space where it should be allocated. This is useful to force
  Pallas to allocate an array in a specific memory space.

  As of now, this only operates on the inputs pallas_calls, as in you can
  apply this to the arguments of a pallas_call and it will constrain them, but
  other operations will not respect this constraint.

  Args:
    x: The array to constrain.
    memory_space: The memory space to constrain to.

  Returns:
    The array ``x`` with the memory space constraint.
  """
  if memory_space is pl_core.MemorySpace.ANY:
    return x
  if memory_space not in {
      tpu_core.MemorySpace.HBM,
      tpu_core.MemorySpace.VMEM,
      tpu_core.MemorySpace.SMEM,
  }:
    raise NotImplementedError(
        "with_memory_space_constraint only supports HBM, VMEM and SMEM."
    )
  return pl_core.with_memory_space_constraint_p.bind(
      x, memory_space=memory_space)

