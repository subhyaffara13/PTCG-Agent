
def _run_serde_pass(
    module: ir.Module, *, serialize: bool, ir_version: int | None = None
) -> ir.Module:
  bytecode_buffer = io.BytesIO()
  module.operation.write_bytecode(bytecode_buffer)
  module = ir.Module.parse(bytecode_buffer.getvalue(), context=module.context)
  pipeline = passmanager.PassManager.parse(
      "builtin.module(mosaic_gpu-serde{serialize="
      + str(serialize).lower()
      + (f" target-version={ir_version}" if ir_version is not None else "")
      + "})",
      module.context,
  )
  allow_unregistered_dialects = module.context.allow_unregistered_dialects
  module.context.allow_unregistered_dialects = True
  try:
    pipeline.run(module.operation)
    module.operation.verify()
  finally:
    module.context.allow_unregistered_dialects = allow_unregistered_dialects
  return module

