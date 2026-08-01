
def _gather_lowering_rule(
    ctx: LoweringRuleContext,
    x,
    indices,
    *,
    dimension_numbers,
    slice_sizes,
    unique_indices,
    indices_are_sorted,
    mode,
    fill_value,
):
  in_aval = ctx.avals_in[0]
  indices_aval = ctx.avals_in[1]
  out_aval = ctx.avals_out[0]

  if (
      len(in_aval.shape) != len(out_aval.shape)
      or indices_aval.shape[:-1] != out_aval.shape
      or indices_aval.shape[-1] != 1
  ):
    raise NotImplementedError("Only take_along_axis-like gathers supported")
  rank = len(out_aval.shape)

  # During lowering jnp.take_along_axis to lax.gather, we append extra dimension
  # to the end of the indices array. We should reshape it back to the original
  # shape before lowering to Mosaic and rely on MLIR canonicalization to remove
  # the reshapes.
  recovered_indices = vector.shape_cast(
      ir.VectorType.get(
          ctx.lowering_context.dynamic_shape_replacement_fn(out_aval.shape),
          indices.type.element_type,
      ),
      indices,
  )
  # Note: current support for lax.gather is still very limited.
  del fill_value

  (
      offset_dims,
      collapsed_slice_dims,
      start_index_map,
      operand_batching_dims,
      start_indices_batching_dims,
  ) = dimension_numbers
  if (
      slice_sizes == (1,) * rank
      and mode
      in (
          lax.GatherScatterMode.FILL_OR_DROP,
          lax.GatherScatterMode.PROMISE_IN_BOUNDS,
      )
      and not offset_dims
      and collapsed_slice_dims == start_index_map
      and operand_batching_dims == start_indices_batching_dims
      and len(collapsed_slice_dims) == 1
      and len(operand_batching_dims) == rank - 1
  ):
    (axis,) = collapsed_slice_dims
    if (
        ctx.lowering_context.kernel_type == tpu_core.CoreType.TC
        and axis < rank - 2
    ):
      raise NotImplementedError(
          "Only gathers along the two minormost dimensions supported on TC"
      )
    return tpu.dynamic_gather(x, recovered_indices, [axis])
  raise NotImplementedError("Unsupported gather")


def _gather_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext, *flat_args, tree
):
  ref, transforms, indices, mask = tree.unflatten(flat_args)
  ref_aval, *_ = tree.unflatten(ctx.avals_in)
  if ref_aval.memory_space not in (
      tpu_core.MemorySpace.VMEM,
      pallas_core.MemorySpace.DEFAULT,
  ):
    raise ValueError(
        f"Gather only supports loading from VMEM, got {ref_aval.memory_space}"
    )
  if transforms:
    ref_block_shape, *_ = ctx.block_shapes
    ref, _ = tc_lowering._transform_ref(
        ref, ref_aval, ref_block_shape, transforms
    )
  [out_aval] = ctx.avals_out
  vec_type = ir.VectorType.get(
      out_aval.shape, sc_lowering._dtype_to_ir_type(ref_aval.dtype)
  )
  return tpu.vector_load_idx(vec_type, ref, indices, mask=mask)

