
def _set_initializing(module: Module, initializing: bool):
  for _, value in graphlib.iter_graph(module, graph=True):
    if isinstance(value, Pytree):
      value._pytree__state._initializing = initializing

