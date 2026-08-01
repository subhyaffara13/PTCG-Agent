
def _ensure_all_layouts_are_set(op: ir.OpView) -> None:
  if inference_utils.should_have_layout(op):
    _ensure_right_number_of_layouts(is_vector, "layouts", "vector", op)
  if inference_utils.should_have_tmem_layout(op):
    _ensure_right_number_of_layouts(_is_tmem_ref, "tmem_layouts", "TMEM ref", op)
  if inference_utils.should_have_transforms(op):
    _ensure_right_number_of_layouts(
        inference_utils.is_transformable_smem_memref, "transforms", "SMEM ref", op,
    )

