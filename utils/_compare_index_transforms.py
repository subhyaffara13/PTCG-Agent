
def _compare_index_transforms(idx_map1, idx_map2, block_idxs_avals) -> bool:
  if idx_map1 is idx_map2:
    return True
  idx_map_jaxpr1 = jax.make_jaxpr(idx_map1)(*block_idxs_avals)
  idx_map_jaxpr2 = jax.make_jaxpr(idx_map2)(*block_idxs_avals)
  return fuser_utils.compare_jaxprs(idx_map_jaxpr1, idx_map_jaxpr2)

