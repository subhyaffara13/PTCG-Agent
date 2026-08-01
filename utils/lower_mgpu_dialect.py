
def lower_mgpu_dialect(
    module: ir.Module,
    launch_context: lc.LaunchContext | None,
    auto_barriers: bool = True,
):
  # TODO(apaszke,bchetioui): Make sure the layouts match.
  # TODO(bchetioui): rethink this API. It doesn't make sense to pass in a full
  # module and to traverse all `gpu.LaunchOp`s if we have a `LaunchContext` that
  # references a single `gpu.LaunchOp`.
  #
  # A `LaunchContext` should have all the information needed to lower a single
  # kernel.
  module.context.append_dialect_registry(mlir_interpreter.upstream_dialects)
  module.context.load_all_available_dialects()
  ctx = _lowering_context(module, launch_context, auto_barriers)
  with ir.InsertionPoint(module.body):
    for op in list(module.body):
      ctx.lower_op(op)

