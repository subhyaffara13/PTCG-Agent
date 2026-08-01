
def _unwrap_block_spec_scalar_prefetch(
    block_spec: pallas_core.BlockSpec,
) -> pallas_core.BlockSpec:
  if block_spec is pallas_core.no_block_spec or block_spec.index_map is None:
    return block_spec

  if id(block_spec) in _unwrap_cache:
    return _unwrap_cache[id(block_spec)]

  def new_index_map(*args):
    scalar_prefetch = _get_scalar_prefetch()
    assert scalar_prefetch is not None
    return block_spec.index_map(*args, *scalar_prefetch)

  out_block_spec = block_spec.replace(index_map=new_index_map)
  _unwrap_cache[id(block_spec)] = out_block_spec
  return out_block_spec

