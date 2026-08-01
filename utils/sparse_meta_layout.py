
def sparse_meta_layout() -> TMEMLayout:
  """A TMEM layout for A sparsity metadata.

  See https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-sparse-matrices-sparsity-selector-kind-tf32-m128-256
  """
  # TODO(apaszke): This does not really describe this layout and we can't do it
  # until we add support for multiple vector dims. Still, it's ok to do for now,
  # because we don't use TMEM layouts for any automatic transformations at the
  # moment and only ever compare it for equality.
  return TMEMLayout(
      fa.Tiling(((TMEM_ROWS, 16), (TMEM_ROWS // 4, 1), (16, 1), (8, 1))),
      warp_dims=(-8,),
      lane_dims=(-2, -4, -6),
      vector_dim=-7,
  )

