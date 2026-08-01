
def _start_lowering(sync_lower):
  """Returns an async start lowering function given a synchronous lowering.

  An async StableHLO collective looks like this:

  > %f = "stablehlo.async_start"(%x) ({
  >   ^bb0(%arg: tensor<2x2xf32>):
  >     %tmp = "stablehlo.all_gather"(%arg) : (tensor<2x2xf32>) ->
  tensor<4x2xf32>
  >     stablehlo.return %tmp : tensor<4x2xf32>
  > }) : (tensor<2x2xf32>) -> !stablehlo.future<tensor<4x2xf32>>
  > %y = "stablehlo.async_done"(%f) : (!stablehlo.future<tensor<4x2xf32>>) ->
  tensor<4x2xf32>

  There is an async_start op with a region that performs and returns the
  synchronous collective. _start_lowering takes in a lowering function for the
  synchronous collective and transforms it into a lowering function for the
  async collective by wrapping everything in an async_start.
  """

  def f(ctx, x, **kwargs):
    (x_aval,) = ctx.avals_in  # e.g., f32[2, 2]
    (out_aval,) = ctx.avals_out  # e.g., # AbstractFuture[f32[4, 2]]
    inner_aval = out_aval.inner_aval  # e.g., f32[4, 2]
    inner_type = mlir.aval_to_ir_type(ctx.module_context, inner_aval)  # e.g., <tensor<4x2xf32>
    # e.g., !stablehlo.future<tensor<4x2xf32>>
    future_type = hlo.FutureType.get([inner_type])
    async_start = hlo.AsyncStartOp(future_type, [x])
    block = async_start.regions[0].blocks.append(x.type)
    with ir.InsertionPoint(block):
      inner_ctx = ctx.replace(
          primitive=None, avals_in=[x_aval], avals_out=[inner_aval]
      )
      results = sync_lower(inner_ctx, block.arguments[0], **kwargs)
      hlo.return_(results)
    return async_start.results

  return f

