
def get_arch() -> Arch:
  ip = ir.InsertionPoint.current
  if ip is None:
    raise ValueError(
        "Cannot retrieve the architecture without an insertion point"
    )
  block = ip.block
  op = block.owner
  while op is not None:
    if op.name == "builtin.module":
      arch_major = op.attributes["mosaic_gpu.arch_major"]
      arch_minor = op.attributes["mosaic_gpu.arch_minor"]
      assert isinstance(arch_major, ir.IntegerAttr)
      assert isinstance(arch_minor, ir.IntegerAttr)
      return Arch(arch_major.value, arch_minor.value)
    op = op.parent
  raise ValueError("Cannot retrieve the architecture: no module found")

