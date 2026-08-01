
def _tmem_ref_from_ir(
    ref: ir.Value, expected_layout: ir.Attribute
) -> tcgen05.TMEMRef:
  """Returns a TMEMRef from an IR value.

  Throws an error if the annotated layout does not match the expected layout.
  """
  if not isinstance(ref.type, ir.MemRefType):
    raise ValueError(f"{ref} is not a memref.")
  mem_ref_ty = ir.MemRefType(ref.type)

  if mem_ref_ty.memory_space != utils.tmem():
    raise ValueError(
        f"{ref} has a memory space {mem_ref_ty.memory_space} that is not TMEM."
    )

  i32 = ir.IntegerType.get_signless(32)
  conversion_cast, [tmem_addr] = _undo_conversion_cast(ref, [i32])

  assert mem_ref_ty.rank == 2
  shape = cast(tuple[int, int], tuple(mem_ref_ty.shape))
  el_ty = mem_ref_ty.element_type
  layout_attr = conversion_cast.attributes["layout"]
  if layout_attr != expected_layout:
    raise ValueError(
        f"{ref} has a layout {layout_attr} that does not match the expected"
        f" layout {expected_layout}."
    )
  layout = layouts_lib.from_layout_attr(layout_attr)
  assert isinstance(layout, fa.TiledLayout)
  tmem_layout = tcgen05.TMEMLayout(
      layout.tiling, layout.warp_dims, layout.lane_dims, layout.vector_dim
  )
  return tcgen05.TMEMRef(tmem_addr, shape, el_ty, tmem_layout)

