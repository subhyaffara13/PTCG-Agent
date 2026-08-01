
def _memory_space_to_mosaic_attribute(
    memory_space: AnyMemorySpace | None,
    kernel_type: tpu_core.CoreType,
) -> ir.Attribute:
  tpu_memory_space = tpu_core.memory_space_to_tpu_memory_space(
      memory_space, kernel_type
  )
  match tpu_memory_space:
    case pallas_core.MemorySpace.ANY:
      return ir.Attribute.parse("#tpu.memory_space<any>")
    case pallas_core.MemorySpace.HOST:
      return ir.Attribute.parse("#tpu.memory_space<host>")
    case tpu_core.MemorySpace() as ms:
      return ir.Attribute.parse(f"#tpu.memory_space<{ms}>")
    case pallas_core.CoreMemorySpace() as cms:
      return ir.Attribute.parse(
          f"#tpu.memory_space<{cms.memory_space}, {cms.mesh.core_type}>"
      )
    case _:
      raise NotImplementedError(f"Invalid memory space: {tpu_memory_space!r}")

