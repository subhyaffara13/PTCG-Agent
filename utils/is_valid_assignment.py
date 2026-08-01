
def is_valid_assignment(var: Variable, layout: Constant) -> bool:
  match layout:
    case RegisterLayout(value=reg_layout):
      assert var.memory_space == MemorySpace.REG
      return _is_valid_register_layout_assignment(var.shape, reg_layout)
    case TMEMLayout(value=tmem_layout):
      assert var.memory_space == MemorySpace.TMEM
      return _is_valid_tmem_layout_assignment(var.shape, tmem_layout)
    case SMEMTransforms(tiling=tiling):
      assert var.memory_space == MemorySpace.SMEM
      if tiling is None:
        return True
      return _is_valid_smem_layout_assignment(var.shape, tiling)
    case _:
      raise ValueError(f"Unsupported layout type: {type(layout)}")

