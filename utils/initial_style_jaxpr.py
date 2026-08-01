
def initial_style_jaxpr(
    fun: Callable, in_tree: PyTreeDef, in_avals: Sequence[core.AbstractValue],
    dbg: core.DebugInfo,
  ) -> tuple[core.Jaxpr, list[Any], PyTreeDef]:
  return _initial_style_jaxpr(fun, in_tree, tuple(in_avals), dbg)

