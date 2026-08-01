
def _dot_general_lowering_rule(
    ctx: LoweringRuleContext,
    x,
    y,
    dimension_numbers,
    precision,
    preferred_element_type,
    **_,
):
  for aval in ctx.avals_in:
    if jnp.issubdtype(aval.dtype, jnp.unsignedinteger):
      raise NotImplementedError(
          f"Unsigned integer dtype {aval.dtype} is not supported for"
          " dot_general (matmul) on the Pallas Mosaic TPU backend because"
          " dot_general interprets all integer inputs as signed. Consider"
          " casting to a signed type before the dot operation."
      )
  (lhs_dims, rhs_dims), _ = dimension_numbers
  (aval_out,) = ctx.avals_out
  out_type = ctx.aval_to_ir_type(aval_out)
  assert isinstance(out_type, ir.ShapedType)
  val_type = ir.ShapedType(out_type).element_type
  if any(
      isinstance(val_type, cls)
      for cls in [
          ir.BF16Type,
          ir.F32Type,
          ir.Float8E5M2Type,
          ir.Float8E4M3FNType,
          ir.Float8E4M3B11FNUZType,
      ]
  ):
    val = ir.FloatAttr.get(val_type, 0.0)
  elif isinstance(val_type, ir.IntegerType):
    val = ir.IntegerAttr.get(val_type, 0)
  else:
    raise NotImplementedError(ctx.avals_out[0].dtype)
  lhs_aval, rhs_aval = ctx.avals_in
  # This is really a matrix-vector product. It only looks like matrix-matrix.
  if (
      lhs_dims == (1,)
      and rhs_dims == (1,)
      and ctx.avals_in[1].shape[0] == 1
      and len(ctx.avals_in[0].shape) == 2
      and len(ctx.avals_in[1].shape) == 2
      and (
          lhs_aval.dtype != jnp.float32
          or rhs_aval.dtype != jnp.float32
      )
  ):
    if ctx.avals_in[0].shape != ctx.avals_in[1].shape:
      bcast_shape = jnp.broadcast_shapes(
          ctx.avals_in[0].shape, ctx.avals_out[0].shape
      )
      bcast_shape = ir.VectorType.get(
          ctx.lowering_context.dynamic_shape_replacement_fn(bcast_shape),
          _dtype_to_ir_type(ctx.avals_out[0].dtype)
      )
      if ctx.avals_in[0].shape != bcast_shape:
        x = vector.broadcast(bcast_shape, x)
      if ctx.avals_in[1].shape != bcast_shape:
        y = vector.broadcast(bcast_shape, y)
    red_dtype = (
        preferred_element_type if preferred_element_type else lhs_aval.dtype
    )
    red_type = ctx.aval_to_ir_type(
        lhs_aval.update(shape=(lhs_aval.shape[0],), dtype=red_dtype),
    )

    if lhs_aval.dtype != red_dtype:
      lhs_type = ctx.aval_to_ir_type(
          lhs_aval.update(shape=lhs_aval.shape, dtype=red_dtype),
      )
      if red_dtype == jnp.float32:
        x = arith.extf(lhs_type, x)
      else:
        raise NotImplementedError(f"Unsupported {preferred_element_type=}")

    if rhs_aval.dtype != red_dtype:
      rhs_type = ctx.aval_to_ir_type(
          rhs_aval.update(shape=rhs_aval.shape, dtype=red_dtype),
      )
      if red_dtype == jnp.float32:
        y = arith.extf(rhs_type, y)
      else:
        raise NotImplementedError(f"Unsupported {preferred_element_type=}")

    acc = arith.constant(
        red_type, ir.DenseElementsAttr.get_splat(red_type, val)
    )
    red = vector.multi_reduction(
        ir.Attribute.parse("#vector.kind<add>"),
        arith.mulf(x, y),
        acc,
        [1]
    )
    return vector.shape_cast(out_type, red)

  tpu_dot_dims = jax_dot_dims_to_tpu_dot_dot_dims(
      dimension_numbers, lhs_aval.shape, rhs_aval.shape
  )

  if precision is not None:
    if precision[0] != precision[1]:
      raise NotImplementedError("Per-operand dot precision unsupported")
    precision = precision[0]
  if precision is None or precision == lax.Precision.DEFAULT:
    precision_attr = None  # That's the default in Mosaic.
  elif precision == lax.Precision.HIGHEST:
    precision_attr = ir.Attribute.parse(
        "#tpu.contract_precision<fp32>"
    )
  else:
    raise NotImplementedError(f"Unsupported dot precision: {precision}")
  out_tile = arith.constant(
      out_type, ir.DenseElementsAttr.get_splat(out_type, val)
  )
  # Contracting second minor is to transpose the lhs. Only try fusing if it's
  # an implicit transpose.
  implicit_transpose = (ctx.avals_in[0].ndim - 2) in lhs_dims
  return tpu.matmul(
      out_type,
      x,
      y,
      out_tile,
      dimension_numbers=tpu_dot_dims,
      precision=precision_attr,
      transpose_lhs_hint=not ctx.forward_compatible
      and ctx.lowering_context.fuse_transposed_lhs_in_matmul
      and implicit_transpose,
  )

