
def _new_ir_context() -> ir.Context:
  ctx = mlir.JaxIrContext()
  ctx.append_dialect_registry(mlir.upstream_dialects)
  tt_dialect.register_dialect(ctx)
  ctx.load_all_available_dialects()
  return ctx

