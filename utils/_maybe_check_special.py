
def _maybe_check_special(outs):
  if not config.debug_nans.value and not config.debug_infs.value: return
  bufs = [s.data for leaf in tree_leaves(outs)
          for s in getattr(leaf, 'addressable_shards', [])]
  try:
    dispatch.check_special('shard_map', bufs)
  except api_util.InternalFloatingPointError as e:
    raise FloatingPointError(f'Invalid value ({e.ty}) encountered in sharded computation.') from None

