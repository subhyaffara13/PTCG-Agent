
def _cudnn_fusion_stablehlo_lowering(ctx, *args, name, jaxpr):
  """Make cudnn_fusion which calls the implementation function.
  Currently this leaks a CallOp since we're using the `core_call_lowering`
  function, but this should get cleaned up by DCE easily.
  """
  impl = mlir.core_call_lowering(
    ctx, *args, name=name + ".impl", call_jaxpr=jaxpr
  )
  call_op = impl[0].owner
  called_fn = call_op.attributes["callee"]
  return hlo.CustomCallOp(
    [r.type for r in call_op.results],
    call_op.operands,
    call_target_name="__cudnn$fusion",
    called_computations=ir.ArrayAttr.get([called_fn]),
  ).results

