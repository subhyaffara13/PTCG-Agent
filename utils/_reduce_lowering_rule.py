
def _reduce_lowering_rule(op, ctx: LoweringRuleContext, x, *, axes, **kwargs):
  [x_aval] = ctx.avals_in
  match x.layout:
    case mgpu.WGStridedFragLayout():
      if set(axes) != set(range(x_aval.ndim)):
        raise NotImplementedError("No support for axes yet")
      # To relax the restriction below, you need to ensure sufficient
      # synchronization with other places that use `scratch_view` (which at the
      # time of writing is only `run_scoped`).
      if ctx.module_ctx.axis_names.wg is not None:
        raise NotImplementedError(
            "No support for reduce_sum over all axes and multiple Pallas"
            " threads"
        )
      scratch_ty = jax.ShapeDtypeStruct(shape=(4,), dtype=x_aval.dtype)
      with ctx.module_ctx.scratch_view(scratch_ty) as scratch:
        return x.reduce(op, axes, scratch)
    case mgpu.TiledLayout():
      if len(axes) != 1:
        raise NotImplementedError("Multi-axis reductions not supported")
      reduced_dim = x.layout.tiling.tile_dimension(axes[0])
      if any(reduced_dim[d] for d in x.layout.partitioned_warp_dims):
        dtype_bitwidth = dtypes.itemsize_bits(x_aval.dtype)
        if dtype_bitwidth % 8:
          raise NotImplementedError("Sub-byte dtypes not supported")
        scratch_elems = ctx.module_ctx.reduction_scratch_bytes * 8 // dtype_bitwidth
        scratch_ty = jax.ShapeDtypeStruct(shape=(scratch_elems,), dtype=x_aval.dtype)
        scratch_ctx = ctx.module_ctx.scratch_view(scratch_ty)
      else:
        scratch_ctx = contextlib.nullcontext(None)
      with scratch_ctx as scratch:
        return x.reduce(op, axes[0], scratch=scratch)
    case _:
      raise NotImplementedError(f"Unsupported layout {x.layout}")

