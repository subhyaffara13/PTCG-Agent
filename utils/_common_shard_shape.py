
def _common_shard_shape(self, global_shape: Shape) -> Shape:
  hlo_sharding = self._to_xla_hlo_sharding(len(global_shape))
  if is_hlo_sharding_replicated(hlo_sharding):
    return global_shape
  if hlo_sharding.is_unreduced():
    return global_shape
  partitions, _ = get_num_ways_dim_sharded(hlo_sharding)
  assert len(partitions) == len(global_shape), (len(partitions), len(global_shape))
  out = []
  for dim, (s, p) in enumerate(safe_zip(global_shape, partitions)):
    quotient, remainder = divmod(s, p)
    if remainder != 0:
      raise IndivisibleError(
          f"Sharding {self} implies that array axis {dim} is partitioned "
          f"{p} times, but the dimension size is {s} "
          f"(full shape: {global_shape}, "
          f"per-dimension tiling factors: {partitions} should evenly divide "
          "the shape)")
    out.append(quotient)
  return tuple(out)

