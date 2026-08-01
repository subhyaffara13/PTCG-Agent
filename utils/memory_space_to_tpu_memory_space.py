
def memory_space_to_tpu_memory_space(
    memory_space: (
        MemorySpace
        | pallas_core.MemorySpace
        | pallas_core.CoreMemorySpace
        | None
    ),
    core_type: CoreType,
) -> MemorySpace | pallas_core.MemorySpace | pallas_core.CoreMemorySpace:
  match memory_space:
    case None:
      match core_type:
        case CoreType.TC:
          return pallas_core.MemorySpace.ANY
        case CoreType.SC_SCALAR_SUBCORE | CoreType.SC_VECTOR_SUBCORE:
          return MemorySpace.HBM
    case pallas_core.MemorySpace.DEFAULT:
      match core_type:
        case CoreType.TC | CoreType.SC_VECTOR_SUBCORE:
          return MemorySpace.VMEM
        case CoreType.SC_SCALAR_SUBCORE:
          return MemorySpace.SMEM
        case _:
          raise ValueError(f"Unsupported core type: {core_type}")
    case pallas_core.MemorySpace.ANY | pallas_core.MemorySpace.HOST:
      return memory_space
    case (
        pallas_core.MemorySpace.ERROR
        | pallas_core.MemorySpace.INDEX
        | pallas_core.MemorySpace.KEY
    ):
      return MemorySpace.SMEM
    case pallas_core.CoreMemorySpace():
      return (
          memory_space.memory_space
          if memory_space.mesh.core_type is core_type
          else memory_space
      )
    case MemorySpace():
      return memory_space
    case _:
      raise ValueError(f"Invalid memory space: {memory_space!r}")

