
def module_to_bytecode(module: ir.Module) -> bytes:
  output = io.BytesIO()
  module.operation.write_bytecode(file=output)
  return output.getvalue()

