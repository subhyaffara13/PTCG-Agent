
def current_context() -> ModuleStackEntry | None:
  return MODULE_CONTEXT.module_stack[-1]

