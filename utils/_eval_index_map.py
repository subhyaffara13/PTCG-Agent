
def _eval_index_map(
    module_ctx: ModuleContext,
    launch_ctx: mgpu.LaunchContext,
    idx: Sequence[ir.Value],
    block_mapping: pallas_core.BlockMapping,
) -> Sequence[ir.Value]:
  block_indices = lower_jaxpr_to_mosaic_gpu(
      module_ctx, launch_ctx, block_mapping.index_map_jaxpr.jaxpr, idx
  )
  result = []
  for i, b in zip(block_indices, block_mapping.block_shape):
    match b:
      case pallas_core.Squeezed() | pallas_core.Element():
        result.append(i)
      case pallas_core.Blocked():
        result.append(arith_dialect.muli(_as_index(i), _as_index(b)))
      case _:
        raise ValueError(f"Unsupported block dim type: {b}")
  return tuple(result)


def _eval_index_map(
    ctx: ModuleContext, idx, block_mapping: BlockMapping
):
  block_indices = lower_jaxpr_to_triton_ir(
      ctx, block_mapping.index_map_jaxpr.jaxpr, None, *idx
  )
  block_indices = tuple(
      _ensure_ir_value(i, jax_core.ShapedArray((), jnp.int32))
      for i in block_indices
  )
  block_indices = tree_util.tree_unflatten(
      block_mapping.index_map_out_tree, block_indices)
  if block_mapping.pipeline_mode is not None:
    raise NotImplementedError(
        "Pipeline mode is not supported in Triton lowering."
    )
  if any(
      isinstance(b, pallas_core.Element) and b.padding != (0, 0)
      for b in block_mapping.block_shape
  ):
    raise NotImplementedError(
        "Unblocked indexing with padding is not supported in Triton lowering."
    )
  def _get_start_index(i, b):
    match b:
      case pallas_core.Squeezed() | pallas_core.Element():
        return i
      case pallas_core.Blocked():
        return _mul(i, _ir_constant(b.block_size, i.type))
      case _:
        raise ValueError(f"Unsupported block dim type: {type(b)}")
  return tuple(
      _get_start_index(i, b) for i, b in
      zip(block_indices, block_mapping.block_shape)
  )

