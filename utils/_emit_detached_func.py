from typing import Callable

def _emit_detached_func(
    name: str,
    input_types: Sequence[ir.Type],
    output_types: Sequence[ir.Type],
    body_builder: Callable[[list[ir.Value]], Sequence[ir.Value]],
) -> func.FuncOp:
  """Helper to emit a detached FuncOp."""
  ftype = ir.FunctionType.get(input_types, output_types)
  func_op = func.FuncOp(name, ftype, ip=False)
  entry_block = func_op.add_entry_block()
  try:
    with ir.InsertionPoint(entry_block):
      outs = body_builder(list(entry_block.arguments))
      func.return_(list(outs))
  except Exception:
    func_op.operation.erase()
    raise
  return func_op

