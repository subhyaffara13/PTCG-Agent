
def cluster_collective_mask(
    cluster_shape: tuple[int, int, int],
    collective: Sequence[gpu.Dimension] | gpu.Dimension,
    leader_tracked: bool = False,
):
  if isinstance(collective, gpu.Dimension):
    collective = (collective,)
  # We first compute the linearized index of the slice along the collective
  # dim that contains the current block. Then, the mask is a sequence of 1s
  # strided by the position of the collective dim, shifted left by the linear
  # slice index.
  # TODO(apaszke): Make sure this gets hoisted outside of any loops.
  # If not, we might need to do it manually.
  i32 = ir.IntegerType.get_signless(32)
  mask_shift = c(0, i32)
  # NOTE: GPU dimensions are minor-to-major.
  cluster_strides = get_contiguous_strides(cluster_shape[::-1])[::-1]
  for stride, cluster_dim in zip(cluster_strides, gpu.Dimension):
    if cluster_dim in collective:
      continue
    if cluster_shape[cluster_dim] != 1:  # Constant-fold multiply by 0.
      dim_idx = arith.index_castui(i32, gpu.cluster_block_id(cluster_dim))
      mask_shift = arith.addi(
          mask_shift,
          arith.muli(dim_idx, c(stride, i32)),
      )
  if leader_tracked:
    mask_unshifted = 1
  else:
    mask_unshifted = 0
    collective_strides = [cluster_strides[d] for d in collective]
    collective_shape = tuple(cluster_shape[d] for d in collective)
    for idx in np.ndindex(collective_shape):
      mask_unshifted |= 1 << sum(i * s for i, s in zip(idx, collective_strides))
  return arith.shli(c(mask_unshifted, i32), mask_shift)

