
def get_min_heads_per_blk(
    num_q_heads, num_combined_kv_heads, q_dtype, kv_dtype
):
  q_packing = get_dtype_packing(q_dtype)
  kv_packing = get_dtype_packing(kv_dtype)

  def can_be_xla_fully_tiled(x, packing):
    if x % packing != 0:
      return False
    x //= packing
    return x in (1, 2, 4, 8) or x % 8 == 0

  # TODO(jevinjiang): support unaligned number of heads!
  if not can_be_xla_fully_tiled(num_combined_kv_heads, kv_packing):
    raise ValueError(
        f"Not implemented: {num_combined_kv_heads=} can not be XLA fully tiled."
    )
  assert num_combined_kv_heads % 2 == 0
  num_kv_heads = num_combined_kv_heads // 2
  assert num_q_heads % num_kv_heads == 0
  ratio = num_q_heads // num_kv_heads
  # TODO(jevinjiang): we can choose smaller tiling for packed type if large
  # second minor tiling is not on.
  max_combined_kv_tiling = 8 * kv_packing
  min_combined_kv_heads = (
      max_combined_kv_tiling
      if num_combined_kv_heads % max_combined_kv_tiling == 0
      else num_combined_kv_heads
  )
  min_q_heads = min_combined_kv_heads // 2 * ratio
  if can_be_xla_fully_tiled(min_q_heads, q_packing):
    return min_q_heads, min_combined_kv_heads
  return num_q_heads, num_combined_kv_heads

