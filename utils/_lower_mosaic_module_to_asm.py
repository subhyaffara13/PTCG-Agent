
def _lower_mosaic_module_to_asm(
    module: ir.Module,
    *,
    ir_version: int | None = None,
) -> tuple[bytes, tuple[bool, bool]]:
  has_communication, has_custom_barrier = tpu.private_has_communication(
      module.operation
  )
  # We'll mutate the module, so clone it
  ctx = module.context
  with ctx, module.operation.location as _:
    module_op = module.operation.clone(ip=False)
    prev_allow_unregistered_dialects = ctx.allow_unregistered_dialects
    ctx.allow_unregistered_dialects = True
    target_version = (
        f"target-version={ir_version}" if ir_version is not None else ""
    )
    try:
      pipeline = PassManager.parse(
          "builtin.module(mosaic-serde{serialize=true " + target_version + "})"
      )
      pipeline.run(module_op)
    finally:
      ctx.allow_unregistered_dialects = prev_allow_unregistered_dialects
    bytecode_buffer = io.BytesIO()
    module_op.write_bytecode(bytecode_buffer, desired_version=0)
    asm = bytecode_buffer.getvalue()
    return asm, (
        has_communication,
        has_custom_barrier,
    )

