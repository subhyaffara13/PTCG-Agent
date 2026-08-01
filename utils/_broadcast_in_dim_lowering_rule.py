
def _broadcast_in_dim_lowering_rule(
    ctx: LoweringRuleContext, val, *, shape, broadcast_dimensions, sharding
):
  del sharding
  (aval_in,) = ctx.avals_in
  (aval_out,) = ctx.avals_out
  if aval_in.shape == shape:
    return val

  if broadcast_dimensions:
    out_shape_list = [1] * len(shape)
    for i, s in zip(broadcast_dimensions, aval_in.shape):
      out_shape_list[i] = s
    out_shape = tuple(out_shape_list)
    out_type = ir.VectorType.get(
        ctx.lowering_context.dynamic_shape_replacement_fn(out_shape),
        _dtype_to_ir_type(aval_out.dtype)
    )
    val = vector.shape_cast(out_type, val)
    if out_shape == aval_out.shape:
      return val
  out_type = ir.VectorType.get(
      ctx.lowering_context.dynamic_shape_replacement_fn(aval_out.shape),
      _dtype_to_ir_type(aval_out.dtype)
  )
  return vector.broadcast(out_type, val)


def _broadcast_in_dim_lowering_rule(
    ctx: LoweringRuleContext,
    x: mgpu.FragmentedArray,
    *,
    broadcast_dimensions,
    shape,
    sharding,
):
  del sharding
  [x_aval] = ctx.avals_in
  [y_aval] = ctx.avals_out
  x = _ensure_fa(x, x_aval.dtype)
  rank_diff = y_aval.ndim - x_aval.ndim
  if (isinstance(x.layout, mgpu.WGSplatFragLayout) and
      broadcast_dimensions == tuple(range(rank_diff, rank_diff + x_aval.ndim))):
    return x.broadcast(shape)
  new_layout = None
  if (
      isinstance(x.layout, mgpu.WGStridedFragLayout)
      and broadcast_dimensions == tuple(range(rank_diff, y_aval.ndim))
  ):
    new_layout = mgpu.WGStridedFragLayout(
        shape=y_aval.shape, vec_size=x.layout.vec_size
    )
    return x.broadcast_in_dim(y_aval.shape, broadcast_dimensions, new_layout)
  if not isinstance(layout := x.layout, mgpu.TiledLayout):
    raise NotImplementedError(f"Unsupported layout: {x.layout}")
  if any(d1 >= d2 for d1, d2 in zip(broadcast_dimensions[:-1], broadcast_dimensions[1:])):
    raise NotImplementedError("broadcast_dimensions must be strictly increasing")
  new_dims = [d for d in range(y_aval.ndim) if d not in broadcast_dimensions]
  if (new_layout := ctx.out_layout_hint) is None:
    candidates = [
      mgpu.WGMMA_LAYOUT,
      mgpu.WGMMA_TRANSPOSED_LAYOUT,
      mgpu.TCGEN05_LAYOUT,
      mgpu.TCGEN05_TRANSPOSED_LAYOUT,
      tcgen05.TMEM_NATIVE_LAYOUT,
    ]
    if y_aval.shape[-1] % 16 == 0:
      candidates.append(tcgen05.fa_m64_collective_layout(y_aval.shape[-1]))
    for candidate in candidates:
      if len(candidate.base_tile_shape) != len(shape):
        continue
      if candidate.reduce(new_dims) == layout:
        if new_layout is None:
          new_layout = candidate
        elif candidate == mgpu.TCGEN05_LAYOUT and new_layout == mgpu.WGMMA_LAYOUT:
          continue  # Choosing WGMMA_LAYOUT for backwards compatibility.
        else:
          raise NotImplementedError(
              "Multiple options for the layout of the broadcast result (found"
              f" at least {new_layout} and {candidate}). Use plgpu.layout_cast"
              " on the output to suggest the desired output layout."
          )
  if new_layout is None:
    raise NotImplementedError(
        "No compatible layout found for the broadcast result. Use"
        " plgpu.layout_cast on the output to suggest the desired output layout."
    )
  return x.broadcast_in_dim(y_aval.shape, broadcast_dimensions, new_layout)


def _broadcast_in_dim_lowering_rule(
    ctx: LoweringRuleContext, x, *, broadcast_dimensions, shape, sharding
):
  del sharding
  x = _ensure_ir_value(x, *ctx.avals_in)
  if not isinstance(x.type, ir.RankedTensorType):
    return _bcast_to(x, shape)
  expand_dims = [i for i in range(len(shape)) if i not in broadcast_dimensions]
  for dim in expand_dims:
    x = _expand_dims(x, dim)
  return _bcast_to(x, shape)

