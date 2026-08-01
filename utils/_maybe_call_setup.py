
def _maybe_call_setup(module: Module):
  if (
    has_setup(module)
    and isinstance(module, Module)
    and not module._pytree__state.is_setup
  ):
    # void parent context
    MODULE_CONTEXT.module_stack.append(
      ModuleStackEntry(module, in_compact=False)
    )
    try:
      module.setup()  # type: ignore[attribute-error]
      module._pytree__state._is_setup = True
    finally:
      MODULE_CONTEXT.module_stack.pop()

