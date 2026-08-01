
def _conjure_tilings_for_smem_ref(
    ref_ty: ir.MemRefType
) -> Iterator[tuple[int, ...]]:
  if len(ref_ty.shape) < 2:
    return
  bitwidth = utils.bitwidth(ref_ty.element_type)
  strides, _ = ref_ty.get_strides_and_offset()
  rank = len(strides)
  dim_order = np.argsort(strides)

  # We want to tile only the last two dimensions.
  if {dim_order[0], dim_order[1]} != {rank - 1, rank - 2}:
    return

  minor_dim = ref_ty.shape[dim_order[0]]
  second_to_minor_dim = ref_ty.shape[dim_order[1]]

  # The second to minor dimension must be tileable by 8.
  if second_to_minor_dim % 8 != 0:
    return

  transposed = dim_order[0] != rank - 1
  for swizzle in [128, 64, 32]:
    swizzle_elems = 8 * swizzle // bitwidth
    if minor_dim % swizzle_elems == 0:
      yield (swizzle_elems, 8) if transposed else (8, swizzle_elems)

