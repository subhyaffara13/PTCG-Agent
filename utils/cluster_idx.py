
def cluster_idx(
    dim: gpu.Dimension | Sequence[gpu.Dimension] | None = None,
    dim_idx: ir.Value | Sequence[ir.Value] | None = None,
) -> ir.Value:
  """Returns the linear index of a block within a subset of the cluster spanned by the given dimensions.

  dim_idx can be used to specify the index of another block along the selected
  dimensions. If not provided, the current block's index is used.
  """
  if dim is None:
    dim = tuple(gpu.Dimension)
  elif isinstance(dim, gpu.Dimension):
    dim = (dim,)
  if dim_idx is None:
    dim_idx = [gpu.cluster_block_id(d) for d in dim]
  elif isinstance(dim_idx, ir.Value):
    if len(dim) != 1:
      raise ValueError(
          "Expected a single dimension when passing a single index"
      )
    dim_idx = [dim_idx]
  index = ir.IndexType.get()
  stride = c(1, index)
  lin_idx = c(0, index)
  for d, idx in sorted(zip(dim, dim_idx, strict=True), key=lambda x: x[0]):
    lin_idx = arith.addi(lin_idx, arith.muli(idx, stride))
    stride = arith.muli(stride, gpu.cluster_dim_blocks(d))
  return lin_idx

