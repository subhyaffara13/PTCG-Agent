
def _canonicalize_ir(
    m_original: ir.Module, ignore_callbacks: IgnoreCallbacks
) -> bytes:
  with m_original.context:
    m = type_cast(ir.Module, m_original.operation.clone())
    passes = pm.PassManager.parse(
        "builtin.module(strip-debuginfo)"
    )
    passes.run(m.operation)
    return _serialize_ir(m, ignore_callbacks)

