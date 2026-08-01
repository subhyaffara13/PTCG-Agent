
def _bind_module(parent: Module, module: Module) -> Module:
  assert parent.scope is not None

  for _, value in reversed(list(graphlib.iter_graph(module, graph=True))):
    if isinstance(value, Module):
      if module.scope is None:
        value.scope = parent.scope.copy()  # type: ignore[attribute-error]
      _maybe_call_setup(value)
  return module

