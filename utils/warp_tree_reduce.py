
def warp_tree_reduce(value, op, group_size):
  """Reduce a value across the warpgroup."""
  assert bytewidth(value.type) == 4
  assert 32 % group_size == 0 and group_size <= 32
  i32 = ir.IntegerType.get_signless(32)
  result = value
  iters = np.log2(group_size)
  if not iters.is_integer():
    raise ValueError(
        f"Warp reduction group size should be a power of 2 (got {group_size})"
    )
  iters = int(iters)
  for i in range(iters):
    other_result = nvvm_shfl_sync(
        result.type,
        c(0xFFFFFFFF, i32),
        result,
        c(1 << i, i32),
        c(0x1F, i32),
        nvvm.ShflKind.bfly
    )
    result = op(result, other_result)

  return result

