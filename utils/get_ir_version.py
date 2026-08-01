
def get_ir_version(ctx: mlir.LoweringRuleContext) -> int | None:
  backend = ctx.module_context.get_backend(optional=True)
  if (
      ctx.is_forward_compat()
      or backend is None
      # TODO(tlongeri, twsung): Remove after 2026-06-05
      or is_cloud_tpu_older_than(2026, 5, 5, backend)
  ):
    return _FWD_COMPAT_VERSION
  # TODO(emilyaf): remove the forward compatibility check after 2026-07-08.
  if is_cloud_tpu_older_than(2026, 6, 8, backend):
    return 13
  return None

