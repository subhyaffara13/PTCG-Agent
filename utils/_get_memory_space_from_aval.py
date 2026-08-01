
def _get_memory_space_from_aval(
    out_aval: jax_core.AbstractValue, kernel_type: tpu_core.CoreType | None
) -> tpu_custom_call.MemorySpace | None:
  if not isinstance(out_aval, jax_core.ShapedArray):
    raise ValueError("Memory spaces not defined for non-ShapedArrays")
  if not isinstance(
      ms := getattr(out_aval, "memory_space", None),
      (
          tpu_core.MemorySpace,
          pallas_core.MemorySpace,
          pallas_core.CoreMemorySpace,
      ),
  ):
    return None  # If we are passed a non-TPU memory space, ignore it.
  # If we are passed an aval with an explicit memory space tag, we use it
  # to constrain the memory space.
  match ms:
    case tpu_core.MemorySpace.HBM:
      return tpu_custom_call.MemorySpace.HBM
    case tpu_core.MemorySpace.VMEM:
      return tpu_custom_call.MemorySpace.VMEM
    case tpu_core.MemorySpace.SMEM:
      return tpu_custom_call.MemorySpace.SMEM
    case tpu_core.MemorySpace.SEMAPHORE:
      match kernel_type:
        case tpu_core.CoreType.SC_SCALAR_SUBCORE:
          return tpu_custom_call.MemorySpace.SC_SCALAR_SEMAPHORE_MEM
        case tpu_core.CoreType.TC:
          return tpu_custom_call.MemorySpace.SEMAPHORE_MEM
        case _:
          raise ValueError(f"Invalid kernel type for semaphore: {kernel_type}")
    case pallas_core.MemorySpace.HOST:
      return tpu_custom_call.MemorySpace.HOST
    case pallas_core.CoreMemorySpace(tpu_core.MemorySpace.VMEM, mesh):
      match mesh.core_type:
        case tpu_core.CoreType.TC:
          return tpu_custom_call.MemorySpace.VMEM
        case _:
          raise ValueError(f"Invalid core type for VMEM: {mesh.core_type}")
    case pallas_core.CoreMemorySpace(tpu_core.MemorySpace.SEMAPHORE, mesh):
      match mesh.core_type:
        case tpu_core.CoreType.SC_SCALAR_SUBCORE:
          return tpu_custom_call.MemorySpace.SC_SCALAR_SEMAPHORE_MEM
        case tpu_core.CoreType.TC:
          return tpu_custom_call.MemorySpace.SEMAPHORE_MEM
        case _:
          raise ValueError(
              f"Invalid core type for semaphore: {mesh.core_type}"
          )
    case _:
      pass
  return None

