
def _serialize_ir(m: ir.Module, ignore_callbacks: IgnoreCallbacks) -> bytes:
  output = io.BytesIO()
  if ignore_callbacks != IgnoreCallbacks.NO:
    m = _remove_callbacks(
        type_cast(ir.Module, m.operation.clone()), ignore_callbacks
    )
  m.operation.write_bytecode(file=output)
  return output.getvalue()

