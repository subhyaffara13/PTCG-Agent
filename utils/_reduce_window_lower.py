
def _reduce_window_lower(
    reduce_op,
    init_value,
    ctx,
    operand,
    *,
    window_dimensions,
    window_strides,
    padding,
    base_dilation,
    window_dilation,
):

  operand_aval, = ctx.avals_in
  scalar_aval = operand_aval.update(
      shape=(), sharding=operand_aval.sharding.update(spec=()))

  return mlir.reduce_window(
      ctx,
      reducer_name=f"reduce_window_{scalar_aval.dtype}_reducer",
      reducer_body=lambda reducer: [reduce_op(*reducer.arguments)],
      operands=[operand],
      init_values=[
          mlir.full_like_aval(ctx, init_value(scalar_aval.dtype), scalar_aval)
      ],
      init_values_avals=[scalar_aval],
      out_avals=ctx.avals_out,
      window_dimensions=window_dimensions,
      window_strides=window_strides,
      base_dilation=base_dilation,
      window_dilation=window_dilation,
      padding=padding,
  )

