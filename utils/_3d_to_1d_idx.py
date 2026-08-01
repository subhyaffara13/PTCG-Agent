
def _3d_to_1d_idx(dim_idx_fn, dim_size_fn):
  i32 = ir.IntegerType.get_signless(32)
  as_i32 = lambda x: arith.index_cast(i32, x)
  idx = as_i32(dim_idx_fn(gpu.Dimension.x))
  stride = as_i32(dim_size_fn(gpu.Dimension.x))
  for dim in (gpu.Dimension.y, gpu.Dimension.z):
    idx = arith.addi(idx, arith.muli(as_i32(dim_idx_fn(dim)), stride))
    stride = arith.muli(stride, as_i32(dim_size_fn(dim)))
  return idx

