
def _find_mgpu_call_in_module(module: ir.Module):
  main_funcs = [
      op
      for op in module.body.operations
      if isinstance(op, func.FuncOp) and op.name.value == "main"
  ]
  # TODO(apaszke): Add support for jax.jit, which will call another function
  # from main.
  if len(main_funcs) != 1:
    raise ValueError("Expected a single function in the kernel module")
  [func_body] = main_funcs[0].body.blocks
  return _find_mgpu_call(func_body, list(func_body.arguments))

