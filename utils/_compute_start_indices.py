
def _compute_start_indices(block_mapping, loop_idx, *args, ctx, token):
  jaxpr = block_mapping.index_map_jaxpr
  token, block_indices = _interpret_jaxpr(
      jaxpr.jaxpr,
      *jaxpr.consts,
      *loop_idx,
      *args,
      ctx=ctx,
      token=token,
  )
  def _get_start_index(i, b):
    match b:
      case pallas_core.Squeezed():
        return i
      case pallas_core.Element():
        return i
      case pallas_core.Blocked():
        return i * b.block_size
      case _:
        raise ValueError(f"Unsupported block dim type: {type(b)}")
  ret = jnp.array(
      tuple(
          _get_start_index(i, b)
          for i, b in zip(block_indices, block_mapping.block_shape)
      ),
      dtype=jnp.int32,
  )
  return token, block_indices, ret

